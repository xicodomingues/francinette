/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/16 14:45:28 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/20 16:37:07 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <string.h>
#include <stdio.h>
#include <unistd.h>

int	ft_putstr(char *str);

int main() {
	ft_putstr("");
	write(1, "--\n", 3);
	ft_putstr("hola!\n");
	char s1[10] = "asdfsfg";
	s1[3] = 11;
	ft_putstr(s1);
}