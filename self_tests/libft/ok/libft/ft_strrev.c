/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrev.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 18:49:17 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 18:50:49 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_strrev(char *str)
{
	size_t	len;
	size_t	i;
	char	temp;

	len = ft_strlen(str) - 1;
	i = 0;
	while (i <= len / 2)
	{
		temp = str[i];
		str[i] = str[len - i];
		str[len - i] = temp;
		i++;
	}
}
