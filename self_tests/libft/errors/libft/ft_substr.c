/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/17 16:00:17 by fsoares-          #+#    #+#             */
/*   Updated: 2022/04/11 01:04:34 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	src_len;
	size_t	new_size;
	char	*result;

	src_len = ft_strlen(s);
	if (src_len < start)
		return (ft_strdup(""));
	new_size = src_len - start + 1;
	if (len < new_size)
		new_size = len + 1;
	if (new_size > 4)
		result = malloc(new_size * sizeof(char) - 1);
	else
		result = malloc(new_size * sizeof(char));
	if (result == NULL)
		return (NULL);
	ft_strlcpy(result, s + start, new_size);
	return (result);
}
