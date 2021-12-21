/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 19:01:09 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/21 07:22:31 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

unsigned int	ft_strlcat(char *dest, char *src, unsigned int n);

void	set_str(char *src, char *dest)
{
	int	pos = 0;

	while (src[pos] != '\0')
	{
		dest[pos] = src[pos];
		pos++;
	}
	dest[pos] = '\0';
}

bool	same_str(char *expected, char *output, int len)
{
	int pos;
	int res;

	res = 1;
	pos = 0;
	while (pos < len)
	{
		char e = expected[pos];
		char o = output[pos];
		if (e != o)
			res = 0;
		pos++;
	}
	return res;
}

void reset_strs(char *a, char *b, char *value)
{
	set_str(value, a);
	set_str(value, b);
}

int main() {
	char *s2 = "aaaaa";
	char s1[100] = "";
	char std_s1[100] = "";
	int n = 0;

	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	unsigned int res = ft_strlcat(s1, s2, n);
	unsigned int std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 2;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 3;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 4;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 5;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 6;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 20;
	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

	n = 2;
	s2 = "xyqwerrturerettw";
	reset_strs(std_s1, s1, "aaaaaaa");
	res = ft_strlcat(s1, s2, n);
	std_res = strlcat(std_s1, s2, n);
	printf("n: %i, same string: yours: '%s':%i, std: '%s':%i, %i\n", n, s1, res, std_s1, std_res, same_str(std_s1, s1, 10));

}