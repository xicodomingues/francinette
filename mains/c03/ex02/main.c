/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 19:01:09 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/21 07:22:25 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

char	*ft_strcat(char *dest, char *src);

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
		{
			printf("in pos %d, expected: %d and got: %d\n",
					pos, e, o);
			res = 0;
		}
		pos++;
	}
	if (!res)
		printf("'%s' : '%s' \n", expected, output);
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

	s2 = "xyz";
	reset_strs(std_s1, s1, "aaaa");
	char *res = ft_strcat(s1, s2);
	char *std_res = strcat(std_s1, s2);
	printf("same string: yours: '%s', std: '%s', %i\n", res, std_res, same_str(std_s1, s1, 10));

	s2 = "";
	reset_strs(std_s1, s1, "aaaa");
	res = ft_strcat(s1, s2);
	std_res = strcat(std_s1, s2);
	printf("same string: yours: '%s', std: '%s': %i\n", res, std_res, same_str(std_res, res, 10));
}