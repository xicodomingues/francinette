#define _GNU_SOURCE
#include <dlfcn.h>
#include <execinfo.h>

#include "utils.h"
#include "color.h"

void *results[1000000];
int res_pos = 0;
int cur_res_pos = 0;

#define MALLOC_LIMIT 1000000
t_node allocations[MALLOC_LIMIT];
int alloc_pos = 0;

static void _add_malloc(void *ptr, size_t size, void *to_return)
{

	t_node new_node = allocations[alloc_pos];
	new_node.freed = false;
	new_node.ptr = ptr;
	new_node.returned = to_return;
	new_node.size = size;

#ifdef __APPLE__
	void *buffer[20];
	int nptrs;
	char **strings;
	nptrs = backtrace(buffer, 20);
	strings = backtrace_symbols(buffer, nptrs);
	new_node.strings = strings;
	new_node.nptrs = nptrs;
#endif

	allocations[alloc_pos] = new_node;
	alloc_pos++;
}

static void _mark_as_free(void *ptr)
{
	int previous_free = false;
	for (int pos = 0; pos < alloc_pos && alloc_pos < MALLOC_LIMIT; pos++)
	{
		t_node temp = allocations[pos];
		if (temp.ptr == ptr)
		{
			if (!temp.freed) {
				allocations[pos].freed = true;
				return;
			}
			else
			{
				previous_free = true;
			}
		}
	}

	if (previous_free)
		fprintf(errors_file, "You are trying to free a pointer that was already freed\n");
}

void *malloc(size_t size)
{
	void *(*libc_malloc)(size_t) = (void *(*)(size_t))dlsym(RTLD_NEXT, "malloc");
	void *p = libc_malloc(size);
	void *to_return = p;
	if (res_pos > cur_res_pos && (long)(results[cur_res_pos]) != 1)
		to_return = results[cur_res_pos];
	else if (size < MALLOC_LIMIT)
	{
		memset(p, 0x11, size);
	}
	cur_res_pos++;
	_add_malloc(p, size, to_return);
	return (to_return);
}

void free(void *p)
{
	void (*libc_free)(void *) = (void (*)(void *))dlsym(RTLD_NEXT, "free");
	_mark_as_free(p);
	libc_free(p);
}

int reset_malloc_mock()
{
	int temp = cur_res_pos;

#ifdef __APPLE__
	for (int i = 0; i < cur_res_pos; i++)
	{
		free(allocations[i].strings);
	}
#endif
	res_pos = 0;
	cur_res_pos = 0;
	alloc_pos = 0;
	return temp;
}

void malloc_set_result(void *res)
{
	results[res_pos++] = res;
}

void malloc_set_null(int nth)
{
	reset_malloc_mock();
	for (int i = 0; i < nth; i++)
		malloc_set_result((void *)1);
	malloc_set_result(NULL);
}

size_t get_malloc_size(void *ptr)
{
	size_t size = 0;
	for (int pos = 0; pos < alloc_pos; pos++)
	{
		t_node temp = allocations[pos];
		if (temp.ptr == ptr)
		{
			if (temp.freed)
				size = temp.size;
			else
				return temp.size;
		}
	}
	return size;
}

void print_mallocs()
{
	int temp = alloc_pos;
	for (int pos = 0; pos < temp; pos++)
	{
		t_node tmp = allocations[pos];
		fprintf(errors_file, "%i: %p - %zu - freed: %i - %p\n", pos, tmp.ptr, tmp.size, tmp.freed, tmp.returned);
	}
}

void save_traces(char **strings, int nptrs)
{
#ifdef __APPLE__
	for (int i = 0; i < nptrs; i++)
	{
		fprintf(errors_file, "%s\n", strings[i]);
	}
	fprintf(errors_file, "\n");
#else
	(void)strings;
	(void)nptrs;
#endif
}

int check_leaks(void *result)
{
	if (result)
		free(result);
	int temp = alloc_pos;
	int res = 1;
	for (int pos = 0; pos < temp; pos++)
	{
		t_node tmp = allocations[pos];
		if (!tmp.freed && tmp.returned)
		{
			if (res)
				error("\n");
			fprintf(errors_file, "Memory leak: %p - %zu bytes\n", tmp.returned, tmp.size);
			fprintf(errors_file, "You failed to free the memory allocated at:\n");
			save_traces(tmp.strings, tmp.nptrs);
			res = 0;
		}
	}
	return res;
}

t_node *get_all_allocs()
{
	t_node *result = calloc(alloc_pos, sizeof(t_node));
	for (int i = 0; i < alloc_pos; i++)
	{
		t_node temp;
		temp.ptr = allocations[i].ptr;
		temp.returned = allocations[i].returned;
		temp.size = allocations[i].size;
		temp.freed = allocations[i].freed;
		temp.nptrs = allocations[i].nptrs;
		temp.strings = calloc(temp.nptrs, sizeof(char *));
		for (int j = 0; j < temp.nptrs; j++)
			temp.strings[j] = strdup(allocations[i].strings[j]);
		result[i] = temp;
	}
	return result;
}

void free_all_allocs(t_node *allocs, int malloc_calls)
{
#ifdef __APPLE__
	for (int i = 0; i < malloc_calls; i++)
	{
		for (int j = 0; j < allocs[i].nptrs; j++)
		{
			free(allocs[i].strings[j]);
		}
		free(allocs[i].strings);
	}
#else
	(void)malloc_calls;
#endif
	free(allocs);
}

void add_trace_to_signature(int offset, t_node *allocs, int n)
{
#ifdef __APPLE__
	for (int i = 0; i < allocs[n].nptrs; i++)
	{
		offset += sprintf(signature + offset, "%s\n", allocs[n].strings[i]);
	}
#else
	(void)offset;
	(void)allocs;
	(void)n;
#endif
}

void show_malloc_stack(void *ptr)
{
	t_node alloc;
	alloc.ptr = NULL;
	for (int pos = 0; pos < alloc_pos; pos++)
	{
		t_node temp = allocations[pos];
		if (temp.ptr == ptr)
		{
			if (temp.freed)
				alloc = temp;
			else
			{
				save_traces(temp.strings, temp.nptrs);
				return;
			}
		}
	}
	if (alloc.ptr != NULL)
		save_traces(alloc.strings, alloc.nptrs);
	else
		fprintf(errors_file, "Could not find the corresponding allocation or the pointer %p\n", ptr);
}