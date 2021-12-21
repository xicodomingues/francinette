/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 14:45:28 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/21 07:22:21 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <string.h>
#include <stdio.h>

int	ft_strncmp(char *s1, char *s2, unsigned int n);

int main() {
	char *str1 = (char *)"xxxxxx";
	char *str2 = (char *)"yyyyyy";
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 20), ft_strncmp(str1, str2, 20));
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 0), ft_strncmp(str1, str2, 0));
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 1), ft_strncmp(str1, str2, 1));

	str1 = "abcadef";
	str2 = "abcad";
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 5), ft_strncmp(str1, str2, 5));
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 6), ft_strncmp(str1, str2, 6));

	str1 = "abcad";
	str2 = "abcadtg";
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 5), ft_strncmp(str1, str2, 5));
	printf("std: %i, yours: %i\n", strncmp(str1, str2, 6), ft_strncmp(str1, str2, 6));

	unsigned char str3[10];
	unsigned char str4[10];
	for (int i = 0; i < 10; i++)
	{
		str3[i] = i + 1;
		str4[i] = i + 1;
	}
	str3[7] = 200;
	printf("std: %i, yours: %i\n",
		strncmp((char *)str3, (char *)str4, 8),
		ft_strncmp((char *)str3, (char *)str4, 8));
}