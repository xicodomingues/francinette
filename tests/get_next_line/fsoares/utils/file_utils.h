
#ifndef FILE_UTILS_H
#define FILE_UTILS_H
#include "utils.h"

#define TEST(title, code)                    \
	BASE_TEST(title, {                       \
		code;                                \
		res = leak_check() && res;           \
		res = null_check_gnl(_title) && res; \
	})

#define test_gnl(fd, expected) res = test_gnl_func(fd, expected, _title) && res;

/* for file tester */
int check_res(int res, char *prefix);
int check_alloc(char *next, char *expected);
int leak_check();
int test_gnl_func(int fd, char *expected, char *input);
int silent_gnl_test(int fd, char *expected);
int null_check_gnl(char *file);

#endif