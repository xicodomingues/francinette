# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: fsoares- <fsoares-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/01/11 18:02:58 by fsoares-          #+#    #+#              #
#    Updated: 2022/01/25 18:51:01 by fsoares-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

SRCS = ft_atoi.c ft_bzero.c ft_calloc.c ft_isalnum.c ft_isalpha.c ft_isascii.c \
		ft_isdigit.c ft_isprint.c ft_isspace.c ft_itoa.c ft_memchr.c \
		ft_memcmp.c ft_memcpy.c ft_memmove.c ft_memset.c ft_putchar_fd.c \
		ft_putendl_fd.c ft_putnbr_fd.c ft_putstr_fd.c ft_split.c ft_strchr.c \
		ft_strdup.c ft_striteri.c ft_strjoin.c ft_strlcat.c ft_strlcpy.c \
		ft_strlen.c ft_strmapi.c ft_strncmp.c ft_strnstr.c ft_strrchr.c \
		ft_strtrim.c ft_substr.c ft_tolower.c ft_toupper.c ft_strrev.c

OBJS = $(SRCS:.c=.o)

BONUS_SRCS = ft_lstadd_back.c ft_lstadd_front.c ft_lstclear.c ft_lstdelone.c \
			ft_lstiter.c ft_lstlast.c ft_lstmap.c ft_lstnew.c ft_lstsize.c

BONUS_OBJS = $(BONUS_SRCS:.c=.o)

GCC = gcc -Wall -Wextra -Werror

NAME = libft.a

.c.o:
			$(GCC) -c $<

$(NAME):	$(OBJS)
			ar rc $(NAME) $(OBJS)

all:		$(NAME)

clean:
			rm -f $(OBJS) $(BONUS_OBJS)

fclean:		clean
			rm -f $(NAME)

re:			fclean all

bonus:		$(OBJS) $(BONUS_OBJS)
			ar rc $(NAME) $(OBJS) $(BONUS_OBJS)

.PHONY:		all clean fclean re bonus
