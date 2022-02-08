
CFLAGS		= -g3 -Wall -Wextra -Werror
STRICT		=
UTILS 		= utils/malloc_mock.c utils/utils.c utils/file_utils.c
TEST_FILES	= ../get_next_line.c ../get_next_line_utils.c
BONUS_FILES = ../get_next_line_bonus.c ../get_next_line_utils_bonus.c

mandatory:
	@clang $(CFLAGS) -O3 -D BUFFER_SIZE=1 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -O3 -D BUFFER_SIZE=10 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -O3 -D BUFFER_SIZE=1000000 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out

bonus:
	@echo "\x1b[33mBONUS!"
	@clang $(CFLAGS) -D BUFFER_SIZE=1 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=10 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test.out && ./test.out < lines_around_10.txt && rm -f test.out

	@clang $(CFLAGS) -D BUFFER_SIZE=1 $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test.out && ./test.out && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=10 $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test.out && ./test.out && rm -f test.out
	@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test.out && ./test.out && rm -f test.out
