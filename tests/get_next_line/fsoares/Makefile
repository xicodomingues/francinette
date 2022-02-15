TIMEOUT		= 10
CFLAGS		= -gfull -fsanitize=address -Wall -Wextra -Werror
STRICT		=
UTILS 		= utils/malloc_mock.c utils/utils.c file_utils.c
TEST_FILES	= ../get_next_line.c ../get_next_line_utils.c
BONUS_FILES	= ../get_next_line_bonus.c ../get_next_line_utils_bonus.c
TIMEOUT_ARG	= -D TIMEOUT=$(TIMEOUT)

ifdef EXEC_STRICT
STRICT		= -D STRICT_MEM
endif

mandatory:
	-@clang $(CFLAGS) -D BUFFER_SIZE=1 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test1.out && ./test1.out < lines_around_10.txt
	-@clang $(CFLAGS) -D BUFFER_SIZE=10 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test2.out && ./test2.out < lines_around_10.txt
	-@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(TEST_FILES) -o test3.out && ./test3.out < lines_around_10.txt

bonus:
	@echo "\x1b[33mBONUS!"
	-@clang $(CFLAGS) -D BUFFER_SIZE=1 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(BONUS_FILES) -o test4.out && ./test4.out < lines_around_10.txt && rm -f test.out
	-@clang $(CFLAGS) -D BUFFER_SIZE=10 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(BONUS_FILES) -o test5.out && ./test5.out < lines_around_10.txt && rm -f test.out
	-@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(TIMEOUT_ARG) $(STRICT) tester.c $(UTILS) $(BONUS_FILES) -o test6.out && ./test6.out < lines_around_10.txt && rm -f test.out

	-@clang $(CFLAGS) -D BUFFER_SIZE=1 $(TIMEOUT_ARG) $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test7.out && ./test7.out && rm -f test.out
	-@clang $(CFLAGS) -D BUFFER_SIZE=10 $(TIMEOUT_ARG) $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test8.out && ./test8.out && rm -f test.out
	-@clang $(CFLAGS) -D BUFFER_SIZE=1000000 $(TIMEOUT_ARG) $(STRICT) bonus.c $(UTILS) $(BONUS_FILES) -o test9.out && ./test9.out && rm -f test.out
