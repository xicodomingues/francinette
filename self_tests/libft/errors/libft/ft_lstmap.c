/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/21 12:39:42 by fsoares-          #+#    #+#             */
/*   Updated: 2022/04/11 00:41:55 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*result;
	t_list	*temp;
	t_list	*prev;

	result = NULL;
	while (lst != NULL)
	{
		temp = ft_lstnew(f(lst->content));
		if (temp == NULL)
		{
			ft_lstclear(&result, del);
			return (NULL);
		}
		if (result == NULL)
			result = temp;
		else
			prev->next = temp;
		prev = temp;
		lst = lst->next;
	}
	return (result);
}
