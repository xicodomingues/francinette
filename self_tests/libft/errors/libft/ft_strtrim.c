/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/12 12:32:09 by fsoares-          #+#    #+#             */
/*   Updated: 2022/02/11 15:56:20 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include "libft.h"

char	*ft_strtrim(char const *s1, char const *set)
{
	int	new_len;
	int	start;

	new_len = ft_strlen(s1) - 1;
	while (new_len >= 0 && ft_strchr(set, s1[new_len]))
		new_len--;
	start = 0;
	while (s1[start] && ft_strchr(set, s1[start]))
	{
		start++;
		new_len--;
	}
	return (ft_substr(s1, start, new_len + 1));
}
