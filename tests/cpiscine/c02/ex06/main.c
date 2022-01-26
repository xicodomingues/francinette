/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 21:49:12 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/15 17:04:04 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <ctype.h>
#include <stdio.h>

int ft_str_is_printable(char *str);

int main(void)
{
	int c;
	int i = 0;
	char str[150];

	for (c = 1; c <= 127; ++c)
		if (isprint(c) != 0)
			str[i++] = c;

	printf("\"\": %i\n", ft_str_is_printable(""));
	printf("\"%s\": %i\n", str, ft_str_is_printable(str));
	printf("with a tab: %i\n", ft_str_is_printable("fs\ts"));

	str[0] = 31;
	str[10] = '\0';
	printf("With the character just before: %i\n", ft_str_is_printable(str));

	str[0] = 127;
	str[10] = '\0';
	printf("With the character just after: %i\n", ft_str_is_printable(str));
}
