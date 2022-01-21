/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/14 13:40:02 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/21 16:06:47 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef UTILS_H
#define UTILS_H

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

#include "libft.h"
#include "color.h"

#define MEM_SIZE 0x100
#define REPETITIONS 1000

extern char function[1000];
extern char signature[10000];
extern int g_offset;
extern char escaped[1000];

#define create_test_ctype(fn)                                                \
	int test_##fn(void)                                                      \
	{                                                                        \
		int c;                                                               \
		int res = 1;                                                         \
		for (c = 0; c <= 0xff && res; c++)                                   \
		{                                                                    \
			if (!fn(c) != !ft_##fn(c))                                       \
			{                                                                \
				printf(CYN "fn_" #fn "(%i: %s)" NC ": std: %i, yours: %i\n", \
					   c, escape_chr(c), fn(c), ft_##fn(c));                 \
				res = 0;                                                     \
			}                                                                \
		}                                                                    \
		if (!fn(EOF) != !ft_##fn(EOF))                                       \
		{                                                                    \
			printf(CYN "fn_" #fn "(EOF)" NC ": std: %i, yours: %i\n",        \
				   fn(EOF), ft_##fn(EOF));                                   \
			res = 0;                                                         \
		}                                                                    \
		return res;                                                          \
	}

#define create_test_val(fn)                                                  \
	int test_##fn(void)                                                      \
	{                                                                        \
		int c;                                                               \
		int res = 1;                                                         \
		for (c = 0; c <= 0xff && res; c++)                                   \
		{                                                                    \
			if (fn(c) != ft_##fn(c))                                         \
			{                                                                \
				printf(CYN "ft_" #fn "(%i: %s)" NC ": std: %i, yours: %i\n", \
					   c, escape_chr(c), fn(c), ft_##fn(c));                 \
				res = 0;                                                     \
			}                                                                \
		}                                                                    \
		if (fn(EOF) != ft_##fn(EOF))                                         \
		{                                                                    \
			printf(CYN "ft_" #fn "(EOF)" NC ": std: %i, yours: %i\n",        \
				   fn(EOF), ft_##fn(EOF));                                   \
			res = 0;                                                         \
		}                                                                    \
		return res;                                                          \
	}

#define test(fn)                                        \
	strcpy(function, #fn);                              \
	if (!test_##fn())                                   \
		printf("%-16s: " BRED "KO" NC "\n", "ft_" #fn); \
	else                                                \
		printf("%-16s: " BGRN "OK" NC "\n", "ft_" #fn);

#define no_test(fn) \
	printf("ft_%-13s: " YEL "No test yet\n" NC, #fn)

#ifdef STRICT_MEM
#define null_check(fn_call, rst)                                            \
	reset_malloc_mock();                                                    \
	fn_call;                                                                \
	int malloc_calls = reset_malloc_mock();                                 \
	for (int i = 0; i < malloc_calls; i++)                                  \
	{                                                                       \
		sprintf(signature + g_offset, NC " NULL check for %ith malloc", i); \
		malloc_set_null(i);                                                 \
		void *res = fn_call;                                                \
		rst = check_leaks(res) && rst;                                      \
		if (res != NULL)                                                    \
			rst = error("Should return NULL\n");                            \
	}

#define null_null_check(fn_call, rst)                                       \
	reset_malloc_mock();                                                    \
	fn_call;                                                                \
	int malloc_calls = reset_malloc_mock();                                 \
	for (int i = 0; i < malloc_calls; i++)                                  \
	{                                                                       \
		sprintf(signature + g_offset, NC " NULL check for %ith malloc", i); \
		fn_call;                                                            \
		malloc_set_null(i);                                                 \
		rst = check_leaks(NULL) && rst;                                     \
	}
#else
#define null_check(fn_call, result)
#define null_null_check(fn_call, result)
#endif

/**
 * @brief given a function call that returns an allocated string and the
 * expected return value, this macro will check that the string returned
 * was the one expected as well as that there are no leaks and that it
 * correctly handles allocation errors
 */
#define check_alloc_str_return(fn_call, exp)                 \
	int result = 1;                                          \
	char *res = fn_call;                                     \
	result = same_string(exp, res);                          \
	result = check_mem_size(res, strlen(exp) + 1) && result; \
	result = check_leaks(res) && result;                     \
	null_check(fn_call, result);                             \
	return result;

void handle_signals();

void print_mem(void *ptr, int size);
void print_mem_full(void *ptr, int size);

char *rand_bytes(char *dest, int len);
char *escape_str(char *src);
char *escape_chr(char ch);
void reset(void *m1, void *m2, int size);
void reset_with(void *m1, void *m2, char *content, int size);

int set_sign(const char *format, ...);
int error(const char *format, ...);

int same_ptr(void *res, void *res_std);
int same_mem(void *expected, void *result, int size);
int same_value(int res, int res_std);
int same_sign(int res, int res_std);
int same_offset(void *start, void *start_std, void *res, void *res_std);
int same_return(void *res, void *dest);
int same_size(void *ptr, void *ptr_std);
int same_string(char *expected, char *actual);

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

#ifndef __APPLE__
size_t strlcat(char *dst, const char *src, size_t size);
size_t strlcpy(char *dst, const char *src, size_t size);
char *strnstr(const char *haystack, const char *needle, size_t len);
#endif

#endif
