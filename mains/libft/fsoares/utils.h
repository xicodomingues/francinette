/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/14 13:40:02 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/17 14:36:16 by fsoares-         ###   ########.fr       */
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

#include "libft.h"
#include "color.h"

#define MEM_SIZE 0x100
#define REPETITIONS 1000

char function[1000];
char escaped[1000];

#define create_test_ctype(fn)                                \
	int test_##fn(void)                                      \
	{                                                        \
		int c;                                               \
		int res = 1;                                         \
		for (c = 0; c <= 0xfff && res; c++)                  \
		{                                                    \
			if (!fn(c) != !ft_##fn(c))                       \
			{                                                \
				printf(#fn "(%i: %s) std: %i, yours: %i\n",  \
					   c, escape_chr(c), fn(c), ft_##fn(c)); \
				res = 0;                                     \
			}                                                \
		}                                                    \
		if (!fn(EOF) != !ft_##fn(EOF))                       \
		{                                                    \
			printf(#fn "(EOF) std: %i, yours: %i\n",         \
				   fn(EOF), ft_##fn(EOF));                   \
			res = 0;                                         \
		}                                                    \
		return res;                                          \
	}

#define create_test_val(fn)                                  \
	int test_##fn(void)                                      \
	{                                                        \
		int c;                                               \
		int res = 1;                                         \
		for (c = 0; c <= 0xfff && res; c++)                  \
		{                                                    \
			if (fn(c) != ft_##fn(c))                         \
			{                                                \
				printf(#fn "(%i: %s) std: %i, yours: %i\n",  \
					   c, escape_chr(c), fn(c), ft_##fn(c)); \
				res = 0;                                     \
			}                                                \
		}                                                    \
		if (fn(EOF) != ft_##fn(EOF))                         \
		{                                                    \
			printf(#fn "(EOF) std: %i, yours: %i\n",         \
				   fn(EOF), ft_##fn(EOF));                   \
			res = 0;                                         \
		}                                                    \
		return res;                                          \
	}

#define test(fn)                                   \
	strcpy(function, #fn);                         \
	if (!test_##fn())                              \
		printf("%-10s: " RED "KO" NC "\n\n", #fn); \
	else                                           \
		printf("%-10s: " GRN "OK" NC "\n", #fn);

#define no_test(fn) \
	printf("%-10s: " YEL "No test yet\n" NC, #fn)

void print_mem(void *ptr, int size);
void print_mem_full(void *ptr, int size);
void set_sigsev();
char *rand_bytes(char *dest, int len);
char *escape_str(char *src);
char *escape_chr(char ch);
void reset(void *m1, void *m2, int size);
void reset_with(void *m1, void *m2, char *content, int size);
int error(const char *format, ...);
int same_ptr(void *res, void *res_std);
int same_mem(void *s, void *r, int size);
int same_value(int res, int res_std);
int same_sign(int res, int res_std);
int same_offset(void *start, void *start_std, void *res, void *res_std);
int same_return(void *res, void *dest);

#endif