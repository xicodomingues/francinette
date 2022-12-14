

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <signal.h>
#include <stdarg.h>
#include <limits.h>
#include <unistd.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <stdbool.h>
#include <time.h>
#include <sys/wait.h>

typedef struct alloc_node t_node;
struct alloc_node
{
	void *ptr;
	void *returned;
	size_t size;
	bool freed;
	char **strings;
	int nptrs;
};

#define _GNU_SOURCE
#include <dlfcn.h>
#include <execinfo.h>

#define P__BRED   "\x1B[1;31m"
#define P__YEL   "\x1B[0;33m"
#define P__CYN   "\x1B[0;36m"
#define P__BWHT   "\x1B[1;37m"
#define P__NC    "\x1B[0m"

void save_traces(char **strings, int nptrs);
int error(const char *format, ...);

char function[1000];
char signature[100000];
int g_offset;
char escaped[1000];
char escaped_div = 2;
int where_buffer = 0;
int g_test = 1;
int child_pid = -1;

FILE *errors_file;

void show_signal_msg(char *message, char *resume, int signal)
{
	fprintf(errors_file, P__BRED "Error" P__NC " in test %i: " P__CYN "%s" P__NC ": " P__BRED "%s"P__NC"\n",
			g_test, signature, message);

#ifdef __APPLE__
	if (signal != SIGALRM)
	{
		void *buffer[20];
		int nptrs = backtrace(buffer, 20);
		char **strings = backtrace_symbols(buffer, nptrs);
		save_traces(strings, nptrs);
	}
#endif

	printf(P__YEL "%i.KO %s\n" P__NC, g_test++, resume);
	exit(signal);
}

void sigsegv(int signal)
{
	show_signal_msg("Segmentation fault!", "Segfault", signal);
}

void sigabort(int signal)
{
	show_signal_msg("Memory problems!", "Abort", signal);
}

void sigbus(int signal)
{
	show_signal_msg("Bus error: Trying to set unwritable memory", "Bus Error", signal);
}

void sigalarm(int signal)
{
	show_signal_msg(("Timeout occurred. You can increase the timeout by executing " P__BWHT "francinette --timeout <number of seconds>" P__NC), "Timeout", signal);
}

void handle_signals()
{
	signal(SIGSEGV, sigsegv);
	signal(SIGABRT, sigabort);
	signal(SIGBUS, sigbus);
	signal(SIGALRM, sigalarm);
	srand((unsigned int)time(NULL));
	srandom((unsigned int)time(NULL));
}

void setup_framework(int argn, char **argv)
{
	(void)argn;
	handle_signals();
	char fn[1000];
	sprintf(fn, "%s.log", argv[0]);
	FILE *final_file = fopen(fn, "a");
	fprintf(final_file, "##==##==##&&##==##==##%s\n", argv[0]);
	errors_file = final_file;
}

int set_signature(const char *format, ...)
{
	va_list args;
	va_start(args, format);
	g_offset = vsprintf(signature, format, args);
	va_end(args);
	return g_offset;
}

int error(const char *format, ...)
{
	fprintf(errors_file, P__BRED "Error" P__NC " in test %i: " P__CYN "%s" P__NC ": ", g_test, signature);
	va_list args;
	va_start(args, format);
	vfprintf(errors_file, format, args);
	va_end(args);
	return 0;
}


void *results[100];
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

void handle_termination(int signal)
{
	(void)signal;
	int res = check_leaks(NULL);
	printf("=====\n==no leaks==: %i\n", res);
	fflush(stdout);
	exit(!res);
}

void reset_mocks(int signal)
{
	(void)signal;
	reset_malloc_mock();
	printf("reseted!!!\n");
	fflush(stdout);
}

int main(int argn, char **args)
{
	setup_framework(argn, (char **)args);
	set_signature("on %s", __FILE__);
	signal(SIGINFO, reset_mocks);
	signal(SIGINT, handle_termination);
	printf("__PID: %i\n", getpid());
	fflush(stdout);

	//**main_here
}