
#ifndef

/* for file tester */
int check_res(int res, char *prefix);
int check_alloc(char *next, char *expected);
int leak_check();
int test_gnl_func(int fd, char *expected, char *input);
int silent_gnl_test(int fd, char *expected);
int null_check_gnl(char *file);