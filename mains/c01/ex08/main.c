/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 15:11:34 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/17 13:18:15 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>

void	ft_sort_int_tab(int *tab, int size);

void	ft_swap(int *a, int *b)
{
	int	temp;

	temp = *a;
	*a = *b;
	*b = temp;
}

void	print_array(int *arr, int size)
{
	int	i;

	i = 0;
	while (i < size)
		printf("%d ", arr[i++]);
	printf("\n");
}

void	shuffle_array(int *arr, int size)
{
	int	counter;

	counter = 0;
	while (counter < size * 5)
	{
		ft_swap(&arr[rand() % size], &arr[rand() % size]);
		counter++;
	}
}

void	populate_array(int *arr, int size)
{
	int	i;

	i = 0;
	while (i < size)
	{
		arr[i] = i + 1;
		i++;
	}
	shuffle_array(arr, size);
}

int	main(void)
{
	int	empty[0];
	int	test_even[10];
	int	test_odd[11];
	int	test_lots[123];

	populate_array(test_even, 10);
	populate_array(test_odd, 11);
	populate_array(test_lots, 123);
	ft_sort_int_tab(empty, 0);
	ft_sort_int_tab(test_even, 10);
	ft_sort_int_tab(test_odd, 11);
	ft_sort_int_tab(test_lots, 123);
	print_array(empty, 0);
	print_array(test_even, 10);
	print_array(test_odd, 11);
	print_array(test_lots, 123);
}
