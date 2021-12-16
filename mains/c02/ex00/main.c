/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42barcel>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/08 18:37:02 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/08 19:11:13 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

char	*ft_strcpy(char *dest, char *src);

int	main(void)
{
	char	dest[20];

	dest[0] = 'f';
	dest[3] = 'd';
	ft_strcpy(dest, "");
	printf("%s\n", dest);
	ft_strcpy(dest, "abc");
	printf("%s\n", dest);
}
