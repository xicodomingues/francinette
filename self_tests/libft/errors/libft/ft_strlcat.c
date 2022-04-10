/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:37:32 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:37:37 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t dstsize)
{
	size_t	len_dst;

	len_dst = ft_strlen(dst);
	if (len_dst > dstsize)
		return (ft_strlen(src) + dstsize);
	else
		return (len_dst + ft_strlcpy(dst + len_dst, src, (dstsize - len_dst)));
}
