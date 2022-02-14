/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   my_utils.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/14 13:40:02 by fsoares-          #+#    #+#             */
/*   Updated: 2022/02/14 20:36:42 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef MY_UTILS_H
#define MY_UTILS_H

#include "utils/utils.h"
#include "libft.h"

#define create_test_ctype(fn)                                                       \
	int test_##fn(void)                                                             \
	{                                                                               \
		int c;                                                                      \
		int res = 1;                                                                \
		for (c = 0; c <= 0xff && res; c++)                                          \
		{                                                                           \
			if (!fn(c) != !ft_##fn(c))                                              \
			{                                                                       \
				fprintf(errors_file,                                                \
						CYN "fn_" #fn "(%i: %s)" NC ": std: %i, yours: %i\n",       \
						c, escape_chr(c), fn(c), ft_##fn(c));                       \
				res = 0;                                                            \
			}                                                                       \
		}                                                                           \
		if (!fn(EOF) != !ft_##fn(EOF))                                              \
		{                                                                           \
			fprintf(errors_file, CYN "fn_" #fn "(EOF)" NC ": std: %i, yours: %i\n", \
					fn(EOF), ft_##fn(EOF));                                         \
			res = 0;                                                                \
		}                                                                           \
		return res;                                                                 \
	}

#define create_test_val(fn)                                                         \
	int test_##fn(void)                                                             \
	{                                                                               \
		int c;                                                                      \
		int res = 1;                                                                \
		for (c = 0; c <= 0xff && res; c++)                                          \
		{                                                                           \
			if (fn(c) != ft_##fn(c))                                                \
			{                                                                       \
				fprintf(errors_file,                                                \
						CYN "ft_" #fn "(%i: %s)" NC ": std: %i, yours: %i\n",       \
						c, escape_chr(c), fn(c), ft_##fn(c));                       \
				res = 0;                                                            \
			}                                                                       \
		}                                                                           \
		if (fn(EOF) != ft_##fn(EOF))                                                \
		{                                                                           \
			fprintf(errors_file, CYN "ft_" #fn "(EOF)" NC ": std: %i, yours: %i\n", \
					fn(EOF), ft_##fn(EOF));                                         \
			res = 0;                                                                \
		}                                                                           \
		return res;                                                                 \
	}

#define test(fn)                                       \
	strcpy(function, #fn);                             \
	errors_file = fopen("errors_" #fn ".log", "w");    \
	if (!test_##fn())                                  \
	{                                                  \
		printf("%-16s: " RED "KO" NC "\n", "ft_" #fn); \
		fprintf(errors_file, "\n");                    \
	}                                                  \
	else                                               \
		printf("%-16s: " GRN "OK" NC "\n", "ft_" #fn); \
	fclose(errors_file);

#define no_test(fn) \
	printf("ft_%-13s: " YEL "No test yet\n" NC, #fn)

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

void handle_signals_with_time();
int set_signature_tn(int test_number, const char *format, ...);

#endif
