/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 14:45:28 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/16 16:38:40 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <string.h>
#include <stdio.h>

int	ft_strcmp(char *s1, char *s2);

int main() {
	char *str0 = "";
	printf("std: %i, mine: %i\n", strcmp(str0, "a"), ft_strcmp(str0, "a"));

	char *str1 = (char *)"abcadef";
	char *str2 = (char *)"abcadef";
	printf("std: %i, mine: %i\n", strcmp(str1, str2), ft_strcmp(str1, str2));

	str1 = "abcadef";
	str2 = "abcad";
	printf("std: %i, mine: %i\n", strcmp(str1, str2), ft_strcmp(str1, str2));

	str1 = "abcad";
	str2 = "abcadtg";
	printf("std: %i, mine: %i\n", strcmp(str1, str2), ft_strcmp(str1, str2));

	unsigned char str3[10];
	unsigned char str4[10];
	for (int i = 0; i < 10; i++)
	{
		str3[i] = i + 1;
		str4[i] = i + 1;
	}
	str3[7] = 200;
	printf("std: %i, mine: %i\n",
		strcmp((char *)str3, (char *)str4),
		ft_strcmp((char *)str3, (char *)str4));
}