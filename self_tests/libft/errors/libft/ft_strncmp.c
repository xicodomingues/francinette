/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:28:18 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:28:21 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	size_t	len;

	len = ft_strlen(s1) + 1;
	if (len < n)
		n = len;
	len = ft_strlen(s2) + 1;
	if (len < n)
		n = len;
	return (ft_memcmp(s1, s2, n));
}
