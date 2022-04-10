/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/12 19:28:45 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:28:44 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *haystack, const char *needle, size_t len)
{
	char	*res;
	size_t	needle_len;
	size_t	i;

	res = (char *)haystack;
	needle_len = ft_strlen(needle);
	if (needle_len == 0)
		return (res);
	i = 0;
	while (*res && i + needle_len <= len)
	{
		if (ft_strncmp(res, needle, needle_len) == 0)
			return (res);
		res++;
		i++;
	}
	return (NULL);
}
