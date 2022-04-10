/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/19 19:00:34 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 15:18:33 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	char	c;
	int		new;

	new = n / 10;
	c = n % 10;
	if (n < 0)
	{
		write(fd, "-", 1);
		new = new * -1;
		c = -c;
	}
	if (new != 0)
		ft_putnbr_fd(new, fd);
	c += '0';
	write(fd, &c, 1);
}
