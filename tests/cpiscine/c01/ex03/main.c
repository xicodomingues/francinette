/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 13:25:38 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 13:34:24 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <stdio.h>

void	ft_div_mod(int a, int b, int *div, int *mod);

int	main(void)
{
	int	a;
	int	b;
	int	div;
	int	mod;

	a = 123;
	b = 10;
	ft_div_mod(a, b, &div, &mod);
	printf("%d %d %d %d\n", a, b, div, mod);
	a = -123;
	b = 15;
	ft_div_mod(a, b, &div, &mod);
	printf("%d %d %d %d\n", a, b, div, mod);
}
