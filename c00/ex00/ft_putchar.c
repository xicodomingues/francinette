/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/12/05 19:09:16 by fsoares-          #+#    #+#             */
/*   Updated: 2021/12/14 18:39:31 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

/**
 * Writes a character to the stdout
 *
 * @param c the character to print
 */
void	ft_putchar(char c)
{
	write(1, &c, 1);
}
