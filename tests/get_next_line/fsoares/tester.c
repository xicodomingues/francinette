#include "utils/utils.h"
#include "../get_next_line.h"

#define CHECK_INTERVAL 100000

#define TEST(title, x)                                         \
	{                                                          \
		int status = 0;                                        \
		int test = fork();                                     \
		if (test == 0)                                         \
		{                                                      \
			g_test = 0;                                        \
			alarm(TIMEOUT_US / 1000000);                       \
			char *_title = title;                              \
			printf(BLU "%-20s" NC ": ", _title);               \
			fflush(stdout);                                    \
			int res = 1;                                       \
			errors_file = fopen("errors.log", "w");            \
			reset_malloc_mock();                               \
			x;                                                 \
			res = leak_check() && res;                         \
			res = null_check_gnl(_title) && res;               \
			printf("\n");                                      \
			if (res)                                           \
				exit(EXIT_SUCCESS);                            \
			else                                               \
				exit(1);                                       \
		}                                                      \
		else                                                   \
		{                                                      \
			waitpid(test, &status, 0);                         \
			if (WIFEXITED(status) && WEXITSTATUS(status) != 0) \
				show_error_file();                             \
		}                                                      \
	}

#define test_gnl(fd, expected) res = test_gnl_func(fd, expected, _title) && res;

int check_res(int res, char *prefix)
{
	if (!res)
		printf(RED "%i.%sKO " NC, ++g_test, prefix);
	else
		printf(GRN "%i.%sOK " NC, ++g_test, prefix);
	fflush(stdout);
	return res;
}

int check_alloc(char *next, char *expected)
{
	int res = 1;
	if (expected != NULL) {
		res = check_mem_size(next, strlen(expected) + 1);
		if (!res)
			fprintf(errors_file, "should reserve space for the string: %s\n", escape_str(expected));
		check_res(res, "ALLOC_");
	}
	return res;
}

int leak_check()
{
	int res = 1;
	res = check_leaks(NULL);
	check_res(res, "LEAKS_");
	return res;
}

int test_gnl_func(int fd, char *expected, char *input)
{
	set_sign("get_next_line(%i: %s)", fd, escape_str(input));

	char *next = get_next_line(fd);
	int res = check_res(same_string(expected, next), "");
	res = check_alloc(next, expected) && res;
	free(next);
	return res;
}

void populate_expected(char *buffer, int n)
{
	int i = 0;
	while(i < n)
	{
		i += sprintf(buffer + i, "0123456789");
	}
	buffer[n] = 0;
}

int null_check_gnl(char *file)
{
#ifdef STRICT_MEM
	printf("NULL_CHECK: ");
	fflush(stdout);
	int fd = open(file, O_RDONLY);
	int lines = 0;
	reset_malloc_mock();
	char *res;
	do {
		res = get_next_line(fd);
		lines++;
	}
	while (res != NULL);
	close(fd);
	int result = 1;
	int total = reset_malloc_mock();
	for (int i = 0; i < total; i++) {
		sprintf(signature + g_offset, NC " NULL check for %ith malloc", i + 1);
		malloc_set_null(i);
		int count = 0;

		int fd = open(file, O_RDONLY);
		do {
			res = get_next_line(fd);
			free(res);
			if (res != NULL)
				count++;
		}
		while (res != NULL);
		close(fd);

		result = check_leaks(NULL) && result;
		if (lines == count)
			result = error("Should exit early and return NULL\n");
	}
	if (result)
		printf(GRN "OK" NC);
	else
		printf(BRED "KO" NC);
	return result;
#else
	(void)file;
	return 1;
#endif
}

int main()
{
	handle_signals();
	printf( BMAG "BUFFER_SIZE" NC ": %i\n", BUFFER_SIZE);
	TEST("Invalid fd", {
		test_gnl(-1, NULL);
		test_gnl(100, NULL);
		int fd = open("empty.txt", O_RDONLY);
		close(fd);
		test_gnl(fd, NULL);
	});

	TEST("empty.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, NULL);
	});

	TEST("1char.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "0");
		test_gnl(fd, NULL);
	});

	TEST("one_line_no_nl.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "abcdefghijklmnopqrstuvwxyz");
		test_gnl(fd, NULL);
	});

	TEST("only_nl.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "\n");
		test_gnl(fd, NULL);
	});

	TEST("multiple_nl.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, NULL);
	});

	TEST("variable_nls.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "\n");
		test_gnl(fd, "0123456789012345678901234567890123456789x2\n");
		test_gnl(fd, "0123456789012345678901234567890123456789x3\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "0123456789012345678901234567890123456789x5\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "0123456789012345678901234567890123456789x8\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "\n");
		test_gnl(fd, "0123456789012345678901234567890123456789x12");
		test_gnl(fd, NULL);
	});

	TEST("lines_around_10.txt", {
		int fd = open(_title, O_RDONLY);
		test_gnl(fd, "0123456789\n");
		test_gnl(fd, "012345678\n");
		test_gnl(fd, "90123456789\n");
		test_gnl(fd, "0123456789\n");
		test_gnl(fd, "xxxx\n");
		test_gnl(fd, NULL);
	});

	TEST("giant_line.txt", {
		int fd = open(_title, O_RDONLY);
		char expected[200000 + 1];
		populate_expected(expected, 200000);
		test_gnl(fd, expected);
		test_gnl(fd, NULL);
	});

	TEST("giant_line_nl.txt", {
		int fd = open(_title, O_RDONLY);
		char expected[200000 + 2];
		populate_expected(expected, 200000);
		expected[200000] = '\n';
		expected[200001] = 0;
		test_gnl(fd, expected);
		test_gnl(fd, "another line!!!");
		test_gnl(fd, NULL);
	});

	// The file being read is 'lines_around_10.txt'
	TEST("stdin", {
		int fd = STDIN_FILENO;
		test_gnl(fd, "0123456789\n");
		test_gnl(fd, "012345678\n");
		test_gnl(fd, "90123456789\n");
		test_gnl(fd, "0123456789\n");
		test_gnl(fd, "xxxx\n");
		test_gnl(fd, NULL);
	});
}