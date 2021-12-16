/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 15:19:05 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 15:19:45 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

void	ft_rev_int_tab(int *tab, int size);

void	print_array(int *arr, int size)
{
	int	i;

	i = 0;
	while (i < size)
		printf("%d ", arr[i++]);
	printf("\n");
}

int	main(void)
{
	int	empty[0];
	int	test_even[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	int	test_odd[11] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

	ft_rev_int_tab(empty, 0);
	ft_rev_int_tab(test_even, 10);
	ft_rev_int_tab(test_odd, 11);
	print_array(empty, 0);
	print_array(test_even, 10);
	print_array(test_odd, 11);
}