#ifndef __UTILS_H_
#define __UTILS_H_

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

#include "color.h"

#define MEM_SIZE 0x100
#define REPETITIONS 1000
#ifndef TIMEOUT
#define TIMEOUT 3
#endif
#ifndef BUFFER_SIZE
#define BUFFER_SIZE 3
#endif

extern char function[1000];
extern char signature[100000];
extern int g_offset;
extern char escaped[100000];
extern FILE *errors_file;
extern int g_test;
extern int child_pid;

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

#ifdef STRICT_MEM

#define BASE_NULL_CHECK(fn_call, rst, leak_check)                                  \
	reset_malloc_mock();                                                           \
	fn_call;                                                                       \
	t_node *allocs = get_all_allocs();                                             \
	int malloc_calls = reset_malloc_mock();                                        \
	int offset = g_offset;                                                         \
	for (int i = 0; i < malloc_calls; i++)                                         \
	{                                                                              \
		offset = sprintf(                                                          \
					 signature + g_offset,                                         \
					 ":\n" MAG "malloc " NC "protection check for %ith malloc:\n", \
					 i + 1) +                                                      \
				 g_offset;                                                         \
		add_trace_to_signature(offset, allocs, i);                                 \
		malloc_set_null(i);                                                        \
		leak_check;                                                                \
	}                                                                              \
	free_all_allocs(allocs, malloc_calls);

#define null_check(fn_call, rst)                 \
	BASE_NULL_CHECK(fn_call, rst, {              \
		void *res = fn_call;                     \
		rst = check_leaks(res) && rst;           \
		if (res != NULL)                         \
			rst = error("Should return NULL\n"); \
	})

#define null_null_check(fn_call, rst)   \
	BASE_NULL_CHECK(fn_call, rst, {     \
		fn_call;                        \
		rst = check_leaks(NULL) && rst; \
	})

#else
#define BASE_NULL_CHECK(fn_call, rst, leak_check)
#define null_check(fn_call, result)
#define null_null_check(fn_call, rst)
#endif

#define TEST_WRAPPER(title, code)                           \
	{                                                       \
		int status = 0;                                     \
		int test = fork();                                  \
		if (test == 0)                                      \
		{                                                   \
			code;                                           \
		}                                                   \
		else                                                \
		{                                                   \
			long total = 0;                                 \
			long interval = 50000;                          \
			while (total < TIMEOUT * 1000000L)              \
			{                                               \
				usleep(interval);                           \
				int c = waitpid(test, &status, WNOHANG);    \
				if (c != 0 && WIFEXITED(status))            \
				{                                           \
					if (WEXITSTATUS(status) != 0)           \
						add_to_error_file();                \
					break;                                  \
				}                                           \
				total += interval;                          \
			}                                               \
			if (total >= TIMEOUT * 1000000L)                \
			{                                               \
				if (waitpid(test, &status, WNOHANG) == 0)   \
				{                                           \
					kill(test, SIGKILL);                    \
					errors_file = fopen("errors.log", "w"); \
					show_timeout();                         \
					fclose(errors_file);                    \
				}                                           \
			}                                               \
		}                                                   \
	}

/**
 * @brief Macro that wraps a get_next_line_test
 */
#define BASE_TEST(title, code)                  \
	TEST_WRAPPER(title, {                       \
		g_test = 1;                             \
		alarm(TIMEOUT);                         \
		char *_title = title;                   \
		printf(BLU "%-20s" NC ": ", _title);    \
		fflush(stdout);                         \
		int res = 1;                            \
		errors_file = fopen("errors.log", "w"); \
		reset_malloc_mock();                    \
		code;                                   \
		fclose(errors_file);                    \
		printf("\n");                           \
		if (res)                                \
			exit(EXIT_SUCCESS);                 \
		else                                    \
			exit(1);                            \
	})

#define BASE_TEST_OFFSET(offset, title, code)         \
	TEST_WRAPPER(title, {                             \
		g_test = 1;                                   \
		alarm(TIMEOUT);                               \
		char *_title = title;                         \
		printf(BLU "%-" #offset "s" NC ": ", _title); \
		fflush(stdout);                               \
		int res = 1;                                  \
		errors_file = fopen("errors.log", "w");       \
		reset_malloc_mock();                          \
		code;                                         \
		fclose(errors_file);                          \
		printf("\n");                                 \
		if (res)                                      \
			exit(EXIT_SUCCESS);                       \
		else                                          \
			exit(1);                                  \
	})

#define test_gnl(fd, expected) res = test_gnl_func(fd, expected, _title) && res;

void show_timeout();
void handle_signals();
void setup_framework(int argn, char **argv);
int show_res(int res, char *prefix);

void print_mem(void *ptr, int size);
void print_mem_full(void *ptr, int size);

char *rand_bytes(char *dest, int len);
char *rand_str(char *dest, int len);
char *escape_str(char *src);
char *escape_chr(char ch);
void reset(void *m1, void *m2, int size);
void reset_with(void *m1, void *m2, char *content, int size);

int set_signature(const char *format, ...);
int error(const char *format, ...);
void add_to_error_file();

int same_ptr(void *res, void *res_std);
int same_mem(void *expected, void *result, int size);
int same_value(int expected, int res);
int same_return_value(int expected, int res);
int same_sign(int expected, int res);
int same_offset(void *expected_start, void *expected_res, void *start, void *res);
int same_return(void *expected, void *res);
int same_size(void *ptr, void *ptr_std);
int same_string(char *expected, char *actual);
char *my_strdup(const char *s1);
char *my_strndup(const char *s1, size_t size);
/**
 * @brief In normal mode makes sure that you reserved enough space.
 * In strict makes sure that you reserved the correct amount of space.
 *
 * @param ptr The pointer to check how much memory was allocated
 * @param expected_size The expected allocated size
 * @return If it passes or fails the test
 */
int check_mem_size(void *ptr, size_t expected_size);

int reset_malloc_mock();
size_t get_malloc_size(void *ptr);
void malloc_set_result(void *res);
void malloc_set_null(int nth);
int check_leaks(void *ptr);
void print_mallocs();
t_node *get_all_allocs();
void free_all_allocs(t_node *allocs, int malloc_calls);
void add_trace_to_signature(int offset, t_node *allocs, int n);
void show_malloc_stack(void *ptr);
void save_traces(char **strings, int nptrs);

#ifndef __APPLE__
size_t strlcat(char *dst, const char *src, size_t size);
size_t strlcpy(char *dst, const char *src, size_t size);
char *strnstr(const char *haystack, const char *needle, size_t len);
#endif

#endif
