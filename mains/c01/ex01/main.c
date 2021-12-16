/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 12:40:24 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 13:12:38 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <stdio.h>

void	ft_ultimate_ft(int *********ptr);

int	main(void)
{
	int	a;
	int	*ptra1;
	int	**ptra2;
	int	***ptra3;
	int	****ptra4;
	int	*****ptra5;
	int	******ptra6;
	int	*******ptra7;
	int	********ptra8;
	int	*********ptra9;

	a = 567;
	ptra1 = &a;
	ptra2 = &ptra1;
	ptra3 = &ptra2;
	ptra4 = &ptra3;
	ptra5 = &ptra4;
	ptra6 = &ptra5;
	ptra7 = &ptra6;
	ptra8 = &ptra7;
	ptra9 = &ptra8;
	ft_ultimate_ft(ptra9);
	printf("%d\n", a);
	a = 234;
	printf("%d\n", a);
	ft_ultimate_ft(ptra9);
	printf("%d", a);
}
