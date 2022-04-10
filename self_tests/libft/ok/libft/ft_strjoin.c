/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:38:06 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:50:27 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	total_len;
	char	*result;

	total_len = ft_strlen(s1) + ft_strlen(s2) + 1;
	result = malloc(total_len * sizeof(char));
	if (result == NULL)
		return (NULL);
	ft_strlcpy(result, s1, total_len);
	ft_strlcat(result, s2, total_len);
	return (result);
}
