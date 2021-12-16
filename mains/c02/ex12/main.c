/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 20:37:38 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/16 12:56:24 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>

void	*ft_print_memory(void *addr, unsigned int size);

int	main(void)
{
	char src[0xFF + 10];
	int	i;

	i = 0;
	while (i <= 0xFF)
	{
		src[i] = i;
		i++;
	}
	src[i] = 0;

	i = 0;
	while (i < 30)
	{
		ft_print_memory((void *)src, i);
		i++;
	}

	ft_print_memory((void *)src, 0x101);
}
