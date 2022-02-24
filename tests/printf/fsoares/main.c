#include "utils/utils.h"
#include "../ft_printf.h"

#define P "%%"
#define F "%c"
#define PF_BUF_SIZE 105
#define MAX(a, b) ((a) > (b) ? a : b)

#define TEST(title, code)                          \
	BASE_TEST(title, {                             \
		int out_pipe[2];                           \
		int saved_stdout;                          \
		char expected[PF_BUF_SIZE] = {0};          \
		char actual[PF_BUF_SIZE] = {0};            \
		int result = 1;                            \
		saved_stdout = dup(STDOUT_FILENO);         \
		if (pipe(out_pipe) != 0)                   \
		{                                          \
			error("Problem setting up the tests"); \
			exit(1);                               \
		}                                          \
		dup2(out_pipe[1], STDOUT_FILENO);          \
		close(out_pipe[1]);                        \
		code;                                      \
		dup2(saved_stdout, STDOUT_FILENO);         \
	})

static int output_fd = -1;

static void cout(const char *f, ...)
{
	va_list ap;

	if (output_fd == -1)
		output_fd = open("/dev/tty", O_RDWR);

	va_start(ap, f);
	vdprintf(output_fd, f, ap);
	va_end(ap);
}

int show_result(int res, char *prefix)
{
	if (!res)
		cout(RED "%i.KO%s " NC, g_test++, prefix);
	else
		cout(GRN "%i.OK%s " NC, g_test++, prefix);
	fflush(stdout);
	return res;
}

#define test_printf(format_str, ...)                                           \
	{                                                                          \
		memset(expected, 0x11, PF_BUF_SIZE);                                   \
		memset(actual, 0x11, PF_BUF_SIZE);                                     \
		int res = 1;                                                           \
		set_signature("printf(%s, "#__VA_ARGS__ ")", escape_str(format_str)); \
		int ex_read;                                                           \
		int act_read;                                                          \
		int expected_ret = printf(format_str, __VA_ARGS__);                    \
		fflush(stdout);                                                        \
		write(1, "", 1);                                                       \
		if ((ex_read = read(out_pipe[0], expected, PF_BUF_SIZE)) == -1)        \
		{                                                                      \
			error("Internal problem, please run the tests again");             \
			exit(-1);                                                          \
		}                                                                      \
		int actual_ret = ft_printf(format_str, __VA_ARGS__);                   \
		fflush(stdout);                                                        \
		write(1, "", 1);                                                       \
		if ((act_read = read(out_pipe[0], actual, PF_BUF_SIZE)) == -1)         \
		{                                                                      \
			error("Internal problem, please run the tests again");             \
			exit(-1);                                                          \
		}                                                                      \
		res = same_value(expected_ret, actual_ret) && res;                     \
		res = same_mem(expected, actual, MAX(ex_read, act_read) + 2) && res;   \
		res = check_leaks(NULL) && res;                                        \
		show_result(res, "");                                                  \
		result = res && result;                                                \
	}

int main(int argn, char **argv)
{
	setup_framework(argn, argv);

	TEST("%c format", {
		test_printf("%c", 'x');
		test_printf(" %c", 'x');
		test_printf("%c ", 'x');
		test_printf(" %c", 'x');
		test_printf("%c%c%c", 'a', '\t', 'b');
	})
}