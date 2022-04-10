/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/20 10:40:06 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 14:33:41 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_back(t_list **list, t_list *new)
{
	t_list	*last;

	last = ft_lstlast(*list);
	if (last == NULL)
		*list = new;
	else
		last->next = new;
}
