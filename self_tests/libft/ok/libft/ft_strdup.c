/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:21:02 by fsoares-          #+#    #+#             */
/*   Updated: 2022/02/11 15:55:53 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

char	*ft_strdup(const char *s1)
{
	size_t	len;
	char	*result;

	len = ft_strlen(s1) + 1;
	result = (char *)malloc(len * sizeof(char));
	if (result == NULL)
		return (result);
	ft_strlcpy(result, s1, len);
	return (result);
}
