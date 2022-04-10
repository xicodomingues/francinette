/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:19:19 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:23:12 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include "libft.h"

void	*ft_calloc(size_t count, size_t size)
{
	void	*temp;

	temp = (malloc(count * size));
	if (temp == NULL)
		return (NULL);
	ft_bzero(temp, count * size);
	return (temp);
}
