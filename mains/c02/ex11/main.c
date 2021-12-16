/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 20:37:38 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/15 21:36:23 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>

void	ft_putstr_non_printable(char *str);

int	main(void)
{
	char src[0xFF + 10];
	int	i;

	i = 1;
	while (i <= 0xFF)
	{
		src[i - 1] = i;
		i++;
	}
	src[i - 1] = 0;

	ft_putstr_non_printable("Coucou\ntu vas bien ?");
	write(1, "\n", 1);
	ft_putstr_non_printable(src);
	write(1, "\n", 1);
}
