TIMEOUT		= 10
CFLAGS		= -g -fsanitize=address -Wall -Wextra -Werror
STRICT		=
UTILS 		= utils/malloc_mock.c utils/utils.c pf_utils.c
PRINTF_LIB	= ../__my_srcs/libftprintf.a
TIMEOUT_ARG	= -D TIMEOUT=$(TIMEOUT)

ifdef EXEC_STRICT
STRICT		= -D STRICT_MEM
endif

# SDK headers shipping w/Xcode 14.1 (22/11/01)
# and later deprecate some functions used here
CFLAGS		+= -Wno-deprecated-declarations

build_m:
	-@$(MAKE) -C ../__my_srcs fclean 1> /dev/null
	-@$(MAKE) -s -C ../__my_srcs all 1> /dev/null
	-@clang $(CFLAGS) $(TIMEOUT_ARG) $(STRICT) $(UTILS) mandatory.c $(PRINTF_LIB) -ldl -o printf.out

build_b:
	-@$(MAKE) -C ../__my_srcs fclean 1> /dev/null
	-@$(MAKE) -s -C ../__my_srcs bonus 1> /dev/null
	-@clang $(CFLAGS) $(TIMEOUT_ARG) $(STRICT) $(UTILS) bonus.c $(PRINTF_LIB) -ldl -o printf_b.out