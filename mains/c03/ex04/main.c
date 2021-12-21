/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 19:01:09 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/21 07:22:29 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

char	*ft_strstr(char *str, char *to_find);

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
	char *s1 = "xxxxxxxx";
	char *s2 = "";

	char *res = ft_strstr(s1, s2);
	char *std_res = strstr(s1, s2);
	printf("return the same positon: %i (yours: '%lu', std: '%lu')\n", res == std_res, res - s1, std_res - s1);

	s1 = "xyxyza";
	s2 = "xyz";
	res = ft_strstr(s1, s2);
	std_res = strstr(s1, s2);
	printf("return the same positon: %i (yours: '%lu', std: '%lu')\n", res == std_res, (res - s1), (std_res - s1));

	s1 = "xyxyaza";
	s2 = "xyz";
	res = ft_strstr(s1, s2);
	std_res = strstr(s1, s2);
	printf("return NULL on no match: %i, %i\n", res == NULL, std_res == NULL);

	s1 = "xyxyza";
	s2 = "";
	res = ft_strstr(s1, s2);
	std_res = strstr(s1, s2);
	printf("return the first position on empty string: %i (yours: '%lu', std: '%lu')\n", res == std_res, (res - s1), (std_res - s1));

	s1 = "";
	s2 = "";
	res = ft_strstr(s1, s2);
	std_res = strstr(s1, s2);
	printf("return same position on both empty strings: %i\n", res == std_res);

	s1 = "";
	s2 = "xxx";
	res = ft_strstr(s1, s2);
	std_res = strstr(s1, s2);
	printf("return NULL if src is empty: %i (yours: '%p', std: '%p')\n", res == std_res, res , std_res);
}