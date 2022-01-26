/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 13:25:38 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 13:42:34 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <stdio.h>

void	ft_ultimate_div_mod(int *a, int *b);

int	main(void)
{
	int	a;
	int	b;

	a = 123;
	b = 10;
	ft_ultimate_div_mod(&a, &b);
	printf("%d %d\n", a, b);
	a = -123;
	b = 15;
	ft_ultimate_div_mod(&a, &b);
	printf("%d %d\n", a, b);
}
