#include "utils/utils.h"
#include "get_next_line.h"

#define TEST(x)                                       \
	{                                                 \
		int status = 0;                               \
		int test = fork();                            \
		if (test == 0)                                \
		{                                             \
			x;                                        \
			exit(EXIT_SUCCESS);                       \
		}                                             \
		else                                          \
		{                                             \
			usleep(TIMEOUT_US);                       \
			if (waitpid(test, &status, WNOHANG) == 0) \
			{                                         \
				kill(test, 9);                        \
				printf(RED "TIMEOUT");                \
			}                                         \
		}                                             \
	}

void test_gnl(int fd, char *expected)
{
	char *next = get_next_line(fd);
	int res = same_string(expected, result);
	res = check_mem_size(res, strlen(expected) + 1) && res;
	res = check_leaks(next) && res;
	if (!res)
		printf(BRED "KO " NC);
	else
		printf(GRN "OK " NC);
}

//Add null check tests

int main()
{
	int fd = 0;
	TEST({
		test_gnl(-1, NULL);
	})
}