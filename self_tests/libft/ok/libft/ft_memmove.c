/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/12 12:55:29 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:35:01 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dst, const void *src, size_t len)
{
	t_byte	*dest;
	t_byte	*source;

	if (src < dst)
		ft_memcpy(dst, src, len);
	else if (src > dst)
	{
		dest = (t_byte *)dst;
		source = (t_byte *)src;
		while (len-- > 0)
		{
			*dest = *source;
			dest++;
			source++;
		}
	}
	return (dst);
}
