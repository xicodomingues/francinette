/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:33:59 by fsoares-          #+#    #+#             */
/*   Updated: 2022/04/11 00:35:29 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *b, int c, size_t len)
{
	t_byte	*mem;

	mem = (t_byte *)b;
	mem[len] = c;
	while (len-- > 0)
		mem[len] = (t_byte)c;
	return (b);
}
