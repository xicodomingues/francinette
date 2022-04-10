/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/21 12:39:42 by fsoares-          #+#    #+#             */
/*   Updated: 2022/01/25 15:17:48 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*result;
	t_list	*temp;
	t_list	*prev;
	void	*content;

	result = NULL;
	while (lst != NULL)
	{
		content = f(lst->content);
		temp = ft_lstnew(content);
		if (temp == NULL)
		{
			del(content);
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
