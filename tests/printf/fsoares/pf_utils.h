#include "utils/utils.h"
#include "../ft_printf.h"

#define PF_BUF_SIZE 1000005
#define MAX(a, b) ((a) > (b) ? a : b)

#define TEST(title, code)                                      \
	BASE_TEST_OFFSET(12, title, {                              \
		fprintf(errors_file, "For " CYN "%s" NC ":\n", title); \
		int out_pipe[2];                                       \
		int saved_stdout;                                      \
		char expected[PF_BUF_SIZE] = {0};                      \
		char actual[PF_BUF_SIZE] = {0};                        \
		saved_stdout = dup(STDOUT_FILENO);                     \
		if (pipe(out_pipe) != 0)                               \
		{                                                      \
			error("Problem setting up the tests");             \
			exit(1);                                           \
		}                                                      \
		dup2(out_pipe[1], STDOUT_FILENO);                      \
		close(out_pipe[1]);                                    \
		code;                                                  \
		dup2(saved_stdout, STDOUT_FILENO);                     \
	})

#define __test_printf(format_str, signature, fn_call, silent)                  \
	{                                                                          \
		memset(expected, 0x11, PF_BUF_SIZE);                                   \
		memset(actual, 0x11, PF_BUF_SIZE);                                     \
		int result = 1;                                                        \
		set_signature("ft_printf(%s%s)", escape_str(format_str), signature);   \
		int ex_read;                                                           \
		int act_read;                                                          \
		int expected_ret = fn_call;                                            \
		fflush(stdout);                                                        \
		write(1, "", 1);                                                       \
		if ((ex_read = read(out_pipe[0], expected, PF_BUF_SIZE)) == -1)        \
		{                                                                      \
			error("Internal problem, please run the tests again");             \
			exit(-1);                                                          \
		}                                                                      \
		int actual_ret = ft_##fn_call;                                         \
		fflush(stdout);                                                        \
		write(1, "", 1);                                                       \
		if ((act_read = read(out_pipe[0], actual, PF_BUF_SIZE)) == -1)         \
		{                                                                      \
			error("Internal problem, please run the tests again");             \
			exit(-1);                                                          \
		}                                                                      \
		result = same_return_value(expected_ret, actual_ret) && result;        \
		result = same_mem(expected, actual, MAX(ex_read, act_read)) && result; \
		result = check_leaks(NULL) && result;                                  \
		if (silent)                                                            \
		{                                                                      \
			if (!result)                                                       \
				show_result(result, "");                                       \
			else                                                               \
				g_test++;                                                      \
		}                                                                      \
		else                                                                   \
			show_result(result, "");                                           \
		res = res && result;                                                   \
	}

#define test_printf(format_str, ...) \
	__test_printf(format_str, ", " #__VA_ARGS__, printf(format_str, __VA_ARGS__), 0);

#define test_printf_noarg(format_str) \
	__test_printf(format_str, "", printf(format_str), 0);

#define test_printf_silent_noarg(format_str) \
	__test_printf(format_str, "", printf(format_str), 1);

#define test_printf_silent(format_str, ...) \
	__test_printf(format_str, ", " #__VA_ARGS__, printf(format_str, __VA_ARGS__), 1);

static int output_fd = -1;

void cout(const char *f, ...);

int show_result(int res, char *prefix);

void pf_setup_framework(int argn, char **argv);