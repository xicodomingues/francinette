#include "utils/file_utils.h"
#include "../get_next_line_bonus.h"
#include <wchar.h>
#include <locale.h>

void populate_expected(char *buffer, int n)
{
	int i = 0;
	while (i < n)
	{
		i += sprintf(buffer + i, "0123456789");
	}
	buffer[n] = 0;
}

char *get_line(int line)
{
	switch (line)
	{
	case 0:
		return "0123456789\n";
	case 1:
		return "012345678\n";
	case 2:
		return "90123456789\n";
	case 3:
		return "0123456789\n";
	case 4:
		return "xxxx\n";
	default:
		return NULL;
	}
}

int main(int argn, char **argv)
{
	setup_framework(argn, argv);
	printf(BMAG "BUFFER_SIZE" NC ": %i\n", BUFFER_SIZE);

	TEST("open, close, open", {
		char *name = "lines_around_10.txt";
		int fd = open(name, O_RDONLY);
		/* 1 */ test_gnl(fd, "0123456789\n");
		/* 2 */ test_gnl(fd, "012345678\n");
		close(fd);
		char *temp;
		do
		{
			temp = get_next_line(fd);
			free(temp);
		} while (temp != NULL);
		/* 3 */ test_gnl(fd, NULL);
		fd = open(name, O_RDONLY);
		/* 4 */ test_gnl(fd, "0123456789\n");
		/* 5 */ test_gnl(fd, "012345678\n");
		/* 6 */ test_gnl(fd, "90123456789\n");
		/* 7 */ test_gnl(fd, "0123456789\n");
		/* 8 */ test_gnl(fd, "xxxx\n");
		/* 9 */ test_gnl(fd, NULL);
	});

	TEST("2 file descriptors", {
		char *name = "lines_around_10.txt";
		int fd_1 = open(name, O_RDONLY);
		int fd_2 = open(name, O_RDONLY);
		/* 1 */ test_gnl(fd_1, "0123456789\n");
		/* 2 */ test_gnl(fd_2, "0123456789\n");
		/* 3 */ test_gnl(fd_1, "012345678\n");
		/* 4 */ test_gnl(fd_2, "012345678\n");
		/* 5 */ test_gnl(fd_2, "90123456789\n");
		/* 6 */ test_gnl(fd_2, "0123456789\n");
		/* 7 */ test_gnl(fd_2, "xxxx\n");
		/* 8 */ test_gnl(fd_2, NULL);
		/* 9 */ test_gnl(fd_1, "90123456789\n");
		/* 10 */ test_gnl(fd_1, "0123456789\n");
		/* 11 */ test_gnl(fd_1, "xxxx\n");
		/* 12 */ test_gnl(fd_1, NULL);
	});

	TEST("multiple fds", {
		char *name = "lines_around_10.txt";

		char expected[200000 + 2];
		populate_expected(expected, 200000);
		expected[200000] = '\n';
		expected[200001] = 0;

		int fd_1 = open(name, O_RDONLY);
		int fd_2 = open(name, O_RDONLY);
		int fd_3 = open(name, O_RDONLY);
		/* 1 */ test_gnl(fd_1, "0123456789\n");
		/* 2 */ test_gnl(fd_2, "0123456789\n");
		/* 3 */ test_gnl(fd_3, "0123456789\n");
		/* 4 */ test_gnl(fd_1, "012345678\n");
		/* 5 */ test_gnl(fd_2, "012345678\n");
		/* 6 */ test_gnl(fd_2, "90123456789\n");

		int fd_4 = open("giant_line_nl.txt", O_RDONLY);
		/* 7 */ test_gnl(fd_2, "0123456789\n");
		/* 8 */ test_gnl(fd_3, "012345678\n");
		/* 9 */ test_gnl(fd_4, expected);
		/* 10 */ test_gnl(fd_2, "xxxx\n");
		/* 11 */ test_gnl(fd_2, NULL);
		/* 12 */ test_gnl(fd_1, "90123456789\n");
		/* 13 */ test_gnl(fd_4, "another line!!!");
		/* 14 */ test_gnl(fd_1, "0123456789\n");
		/* 15 */ test_gnl(fd_4, NULL);
		/* 16 */ test_gnl(fd_1, "xxxx\n");
		/* 17 */ test_gnl(fd_4, NULL);
		/* 18 */ test_gnl(fd_3, "90123456789\n");
		/* 19 */ test_gnl(fd_3, "0123456789\n");
		/* 20 */ test_gnl(fd_1, NULL);
		/* 21 */ test_gnl(fd_3, "xxxx\n");
		/* 22 */ test_gnl(fd_3, NULL);
	});

	printf("\n");
}
