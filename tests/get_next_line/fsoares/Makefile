
CFLAGS		= -g3 -Wall -Wextra -Werror
STRICT		=
MY_FILES	= tester.c utils/malloc_mock.c utils/utils.c utils/file_utils.c
TEST_FILES	= ../get_next_line.c ../get_next_line_utils.c

all:
	@clang $(CFLAGS) -D BUFFER_SIZE=1 $(STRICT) $(MY_FILES) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=10 $(STRICT) $(MY_FILES) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(STRICT) $(MY_FILES) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
