TIMEOUT_US	= 5000000
BUFFER_SIZE	= 10

CFLAGS		= -g3 -Wall -Wextra -Werror
STRICT		=
PARAMS		= -D TIMEOUT_US=$(TIMEOUT_US) -D BUFFER_SIZE=$(BUFFER_SIZE) $(STRICT)
MY_FILES	= tester.c utils/malloc_mock.c utils/utils.c
TEST_FILES	= ../get_next_line.c ../get_next_line_utils.c

10:
	@clang $(CFLAGS) $(PARAMS) $(MY_FILES) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
