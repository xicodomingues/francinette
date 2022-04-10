/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:34:48 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:34:50 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dst, const void *src, size_t n)
{
	t_byte	*dest;
	t_byte	*source;

	if (dst == src)
		return (dst);
	dest = (t_byte *)dst;
	source = (t_byte *)src;
	while (n-- > 0)
		dest[n] = source[n];
	return (dest);
}
