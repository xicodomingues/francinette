#define _GNU_SOURCE
#include <dlfcn.h>
#include <execinfo.h> //TODO: make work on mac?

#include "utils.h"

typedef struct node t_node;

struct node {
	void *ptr;
	void *returned;
	size_t size;
	bool freed;
};

void *results[100];
int res_pos = 0;
int cur_res_pos = 0;

t_node *head = NULL;
t_node *last = NULL;

t_node allocations[10000];
int alloc_pos = 0;

static void _add_malloc(void *ptr, size_t size, void *to_return)
{
	t_node new_node = allocations[alloc_pos];
	new_node.freed = false;
	new_node.ptr = ptr;
	new_node.returned = to_return;
	new_node.size = size;
	allocations[alloc_pos] = new_node;
	alloc_pos++;
}

static void _mark_as_free(void *ptr)
{
	for (int pos = 0; pos < alloc_pos; pos++) {
		t_node temp = allocations[pos];
		if (temp.ptr == ptr)
			 allocations[pos].freed = true;
	}
}

void * malloc(size_t size)
{
    void *(*libc_malloc)(size_t) = (void *(*)(size_t))dlsym(RTLD_NEXT, "malloc");
    void *p = libc_malloc(size);
	void *to_return = p;
	if (res_pos > cur_res_pos && (long)(results[cur_res_pos]) != 1)
		to_return = results[cur_res_pos];
	cur_res_pos++;
    _add_malloc(p, size, to_return);
    return (to_return);
}

void free(void * p)
{
    void (*libc_free)(void*) = (void (*)(void *))dlsym(RTLD_NEXT, "free");
	_mark_as_free(p);
    libc_free(p);
}

int reset_malloc_mock()
{
	int temp = cur_res_pos;
	res_pos = 0;
	cur_res_pos = 0;
	alloc_pos = 0;
	return temp;
}

void malloc_set_result(void *res) {
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
	for (int pos = 0; pos < alloc_pos; pos++) {
		t_node temp = allocations[pos];
		if (temp.ptr == ptr)
			return temp.size;
	}
	return 0;
}

int check_leaks(void *result)
{
	if (result)
		free(result);
	int temp = alloc_pos;
	int res = 1;
	for (int pos = 0; pos < temp; pos++) {
		t_node temp = allocations[pos];
		if (!temp.freed && temp.returned) {
			error("Memory leak: %p - %zu bytes (%p)\n", temp.returned, temp.size);
			res = 0;
		}
	}
	return res;
}
