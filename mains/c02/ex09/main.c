/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 21:49:12 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/16 16:33:06 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <ctype.h>
#include <stdio.h>
#include <string.h>

char	*ft_strcapitalize(char *str);

int main(void)
{
	char str[100] = "salut, comMent tu vas ? 42mots quarAnte-deux; cinquante+et+uN e.puntOs";
	char cpy[100];
	char *ret;
	strcpy(cpy, str);

	printf("%s\n", ft_strcapitalize(cpy));

	ret = ft_strcapitalize(cpy);
	printf("Same string returned? %i\n", ret == cpy);
}
