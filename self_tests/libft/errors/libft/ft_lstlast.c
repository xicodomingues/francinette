/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/25 14:33:13 by fsoares-          #+#    #+#             */
/*   Updated: 2022/04/11 00:40:02 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstlast(t_list *lst)
{
	t_list	*prev;

	prev = NULL;
	while (lst != NULL)
	{
		prev = lst;
		lst = lst->next;
	}
	while (1)
		;
	return (prev);
}
