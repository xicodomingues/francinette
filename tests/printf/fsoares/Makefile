TIMEOUT		= 10
CFLAGS		= -gfull -fsanitize=address -Wall -Wextra -Werror
STRICT		=
UTILS 		= utils/malloc_mock.c utils/utils.c main.c
TEST_FILES	= ../get_next_line.c ../get_next_line_utils.c
BONUS_FILES	= ../get_next_line_bonus.c ../get_next_line_utils_bonus.c
TIMEOUT_ARG	= -D TIMEOUT=$(TIMEOUT)

ifdef EXEC_STRICT
STRICT		= -D STRICT_MEM
endif

mandatory:
	-@clang $(CFLAGS) $(TIMEOUT_ARG) $(STRICT) $(UTILS) $(TEST_FILES) -o test1.out && ./test1.out < lines_around_10.txt


# TODO: setup makefile
