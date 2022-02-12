/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_mymalloc.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/18 22:51:12 by fsoares-          #+#    #+#             */
/*   Updated: 2022/02/11 21:29:31 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdio.h>
#include <stdlib.h>
#include <execinfo.h>

void	*my_malloc(size_t size)
{
	void	*buffer[100];
	int		nptrs;
	char	**strings;
	int		j;

	nptrs = backtrace(buffer, 100);
	printf("New malloc call!\n");
	strings = backtrace_symbols(buffer, nptrs);
	if (strings == NULL)
	{
		perror("backtrace_symbols");
		exit(EXIT_FAILURE);
	}
	j = 0;
	while (j < nptrs)
		printf("%s\n", strings[j++]);
	return (malloc(size));
}
