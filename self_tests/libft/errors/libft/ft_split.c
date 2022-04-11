/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/19 15:03:04 by fsoares-          #+#    #+#             */
/*   Updated: 2022/04/11 14:03:29 by fsoares-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include "libft.h"

int	count_words(char const *str, char ch)
{
	int	words;
	int	in_word;
	int	i;

	if (str == NULL)
		return (0);
	i = 0;
	in_word = 0;
	words = 0;
	while (str[i] != '\0')
	{
		if (str[i] == ch && in_word)
			in_word = 0;
		if (str[i] != ch && !in_word)
		{
			in_word = 1;
			words++;
		}
		i++;
	}
	return (words);
}

int	populate(char const *s, char **result, int i, char ch)
{
	int	offset;
	int	w_size;

	offset = 0;
	while (s[offset] == ch)
		offset++;
	w_size = 0;
	while (s[offset + w_size] && s[offset + w_size] != ch)
		w_size++;
	result[i] = ft_substr(s, offset, w_size);
	if (result[i] == NULL)
		return (-1);
	return (offset + w_size);
}

char	**clear_result(char **result, int i)
{
	int	j;

	j = 0;
	while (j < i)
	{
		free(result[j]);
		j++;
	}
	free(result);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	int		n_words;
	char	**result;
	int		i;
	int		offset;
	int		temp;

	n_words = count_words(s, c);
	result = malloc((n_words + 2) * sizeof(char *));
	if (result == NULL)
		return (NULL);
	i = 0;
	offset = 0;
	while (i < n_words)
	{
		temp = populate(s + offset, result, i, c);
		offset += temp;
		i++;
	}
	return (result);
}
