/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 21:49:12 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/15 18:19:52 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <ctype.h>
#include <stdio.h>
#include <string.h>

char	*ft_strlowcase(char *str);

int main(void)
{
	char str[100] = "ABDSDF-sdfsdf,,sdfYU74rff;";
	char cpy[100];
	char *ret;
	strcpy(cpy, str);

	printf("\"%s\": %s\n", str, ft_strlowcase(cpy));

	ret = ft_strlowcase(cpy);
	printf("Same string returned? %i\n", ret == cpy);
}
