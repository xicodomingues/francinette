/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 14:45:28 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/20 17:57:05 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <string.h>
#include <stdio.h>

int	ft_strlen(char *str);

int main() {
	char *s = "";
	printf("len of: '%s': %i\n", s, ft_strlen(s));
	s = "sggdsdsg";
	printf("len of: '%s': %i\n", s, ft_strlen(s));
	char s1[10] = "asdfsfg";
	s1[3] = 11;
	printf("len of: '%s': %i\n", s1, ft_strlen(s1));
}