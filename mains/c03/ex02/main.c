/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 19:01:09 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/16 19:23:35 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

char	*ft_strncat(char *dest, char *src, unsigned int nb);

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
	char *src = "aaaaa";
	char dest[100];
	char std_dest[100];

	src = "aaa";
	reset_strs(std_dest, dest, "qwer");
	char *res = ft_strncat(dest, src, 0);
	char *std_res = strncat(std_dest, src, 0);
	printf("same string: mine: '%s', std: '%s': %i\n", ft_strncat(dest, src, 0), strncat(std_dest, src, 0), same_str(std_res, res, 10));

	src = "aaa";
	reset_strs(std_dest, dest, "qwer");
	res = ft_strncat(dest, src, 1);
	std_res = strncat(std_dest, src, 1);
	printf("same string: mine: '%s', std: '%s': %i\n", ft_strncat(dest, src, 0), strncat(std_dest, src, 0), same_str(std_res, res, 10));

	src = "aaa";
	reset_strs(std_dest, dest, "qwer");
	res = ft_strncat(dest, src, 3);
	std_res = strncat(std_dest, src, 3);
	printf("same string: mine: '%s', std: '%s': %i\n", ft_strncat(dest, src, 0), strncat(std_dest, src, 0), same_str(std_res, res, 10));

	src = "aaa";
	reset_strs(std_dest, dest, "qwer");
	res = ft_strncat(dest, src, 4);
	std_res = strncat(std_dest, src, 4);
	printf("same string: mine: '%s', std: '%s': %i\n", ft_strncat(dest, src, 0), strncat(std_dest, src, 0), same_str(std_res, res, 10));

	src = "aaa";
	reset_strs(std_dest, dest, "qwer");
	res = ft_strncat(dest, src, 5);
	std_res = strncat(std_dest, src, 5);
	printf("same string: mine: '%s', std: '%s': %i\n", ft_strncat(dest, src, 0), strncat(std_dest, src, 0), same_str(std_res, res, 10));
}