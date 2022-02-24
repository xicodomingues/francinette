TIMEOUT		= 10
CFLAGS		= -gfull -fsanitize=address -Wall -Wextra -Werror
STRICT		=
UTILS 		= utils/malloc_mock.c utils/utils.c pf_utils.c mandatory.c
PRINTF_LIB	= ../__my_srcs/libftprintf.a
TIMEOUT_ARG	= -D TIMEOUT=$(TIMEOUT)

ifdef EXEC_STRICT
STRICT		= -D STRICT_MEM
endif

build:
	-@$(MAKE) -C ../__my_srcs fclean  1> /dev/null
	-@$(MAKE) -s -C ../__my_srcs 1> /dev/null
	-@clang $(CFLAGS) $(TIMEOUT_ARG) $(STRICT) $(UTILS) $(PRINTF_LIB) -o printf.out && ./printf.out
