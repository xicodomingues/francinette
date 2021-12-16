/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42barcel>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 21:49:12 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 22:03:47 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_str_is_numeric(char *str);

int main(void)
{
	printf("\"123\": %i\n", ft_str_is_numeric("123"));
	printf("\"\": %i\n", ft_str_is_numeric(""));
	printf("\"1234567a89\": %i\n", ft_str_is_numeric("1234567a89"));
}
