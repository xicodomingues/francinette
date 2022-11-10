
#ifndef FILE_UTILS_H
#define FILE_UTILS_H
#include "utils/utils.h"

#define TEST(title, code)                    \
	BASE_TEST(title, {                       \
		code;                                \
		res = leak_check() && res;           \
		res = null_check_gnl(_title) && res; \
	})

#define test_gnl(fd, expected) res = test_gnl_func(fd, expected, _title) && res;
#define test_gnl_limits(fd, expected, line, content) res = test_gnl_func_limits(fd, expected, line, content, _title) && res;


extern int next_read_error;

/* for file tester */
int leak_check();
int test_gnl_func(int fd, char *expected, char *input);
int test_gnl_func_limits(int fd, char *expected, int line, char *content, char *input);
int silent_gnl_test(int fd, char *expected);
int null_check_gnl(char *file);
void print_file_content(char * content);

#endif