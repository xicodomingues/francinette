#include "utils/utils.h"

void populate_expected(char *buffer, int n)
{
	int i = 0;
	while(i < n)
	{
		i += sprintf(buffer + i, "0123456789");
	}
	buffer[n] = 0;
}

int main()
{
	handle_signals();
	printf(BMAG "BUFFER_SIZE" NC ": %i\n", BUFFER_SIZE);
	TEST("Invalid fd", {
		/* 1 */ test_gnl(-1, NULL);
		/* 2 */ test_gnl(100, NULL);
		int fd = open("empty.txt", O_RDONLY);
		close(fd);
		/* 3 */ test_gnl(fd, NULL);
	});

	TEST("empty.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, NULL);
		/* 2 */ test_gnl(fd, NULL);
	});

	TEST("1char.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "0");
		/* 2 */ test_gnl(fd, NULL);
	});

	TEST("one_line_no_nl.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "abcdefghijklmnopqrstuvwxyz");
		/* 2 */ test_gnl(fd, NULL);
	});

	TEST("only_nl.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "\n");
		/* 2 */ test_gnl(fd, NULL);
	});

	TEST("multiple_nl.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "\n");
		/* 2 */ test_gnl(fd, "\n");
		/* 3 */ test_gnl(fd, "\n");
		/* 4 */ test_gnl(fd, "\n");
		/* 5 */ test_gnl(fd, "\n");
		/* 6 */ test_gnl(fd, NULL);
	});

	TEST("variable_nls.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "\n");
		/* 2 */ test_gnl(fd, "0123456789012345678901234567890123456789x2\n");
		/* 3 */ test_gnl(fd, "0123456789012345678901234567890123456789x3\n");
		/* 4 */ test_gnl(fd, "\n");
		/* 5 */ test_gnl(fd, "0123456789012345678901234567890123456789x5\n");
		/* 6 */ test_gnl(fd, "\n");
		/* 7 */ test_gnl(fd, "\n");
		/* 8 */ test_gnl(fd, "0123456789012345678901234567890123456789x8\n");
		/* 9 */ test_gnl(fd, "\n");
		/* 10 */ test_gnl(fd, "\n");
		/* 11 */ test_gnl(fd, "\n");
		/* 12 */ test_gnl(fd, "0123456789012345678901234567890123456789x12");
		/* 13 */ test_gnl(fd, NULL);
	});

	TEST("lines_around_10.txt", {
		int fd = open(_title, O_RDONLY);
		/* 1 */ test_gnl(fd, "0123456789\n");
		/* 2 */ test_gnl(fd, "012345678\n");
		/* 3 */ test_gnl(fd, "90123456789\n");
		/* 4 */ test_gnl(fd, "0123456789\n");
		/* 5 */ test_gnl(fd, "xxxx\n");
		/* 6 */ test_gnl(fd, NULL);
	});

	TEST("giant_line.txt", {
		int fd = open(_title, O_RDONLY);
		char expected[200000 + 1];
		populate_expected(expected, 200000);
		/* 1 */ test_gnl(fd, expected);
		/* 2 */ test_gnl(fd, NULL);
	});

	TEST("giant_line_nl.txt", {
		int fd = open(_title, O_RDONLY);
		char expected[200000 + 2];
		populate_expected(expected, 200000);
		expected[200000] = '\n';
		expected[200001] = 0;
		/* 1 */ test_gnl(fd, expected);
		/* 2 */ test_gnl(fd, "another line!!!");
		/* 3 */ test_gnl(fd, NULL);
	});

	// The file being read is 'lines_around_10.txt'
	TEST("stdin", {
		int fd = STDIN_FILENO;
		/* 1 */ test_gnl(fd, "0123456789\n");
		/* 2 */ test_gnl(fd, "012345678\n");
		/* 3 */ test_gnl(fd, "90123456789\n");
		/* 4 */ test_gnl(fd, "0123456789\n");
		/* 5 */ test_gnl(fd, "xxxx\n");
		/* 6 */ test_gnl(fd, NULL);
	});

	printf("\n");
}