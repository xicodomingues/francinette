/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/19 17:19:00 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 18:50:47 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	create_number(int nb, char *nbr_str, int pos)
{
	char	c;
	int		new;

	new = nb / 10;
	c = nb % 10;
	if (nb < 0)
	{
		nbr_str[pos++] = '-';
		new = new * -1;
		c = -c;
	}
	if (new != 0)
		create_number(new, nbr_str, pos + 1);
	c += '0';
	nbr_str[pos] = c;
}

char	*ft_itoa(int n)
{
	char	digits[20];

	ft_bzero(digits, 20);
	create_number(n, digits, 0);
	if (n < 0)
		ft_strrev(digits + 1);
	else
		ft_strrev(digits);
	return (ft_strdup(digits));
}
