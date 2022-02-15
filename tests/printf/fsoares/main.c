#include "utils/utils.h"
#include "../"

#define TEST(title, code) \
	BASE_TEST(title, {    \
		code;             \
	})

#define test_printf(format) res = _test_printf(format) && res;

#define P "%%"
#define F "%c"
#define PF_BUF_SIZE 105
#define MAX(a, b) ((a) > (b) ? a : b)

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

int _test_printf(char format)
{
	char format_buffer[1000];
	const char test_strs[][100] = {
		P F,
		P P F,
		P P P F,
		P P " " F,
		F P,
		"\0" P F,
		"==-" P F "---",
		P "-" F,
		P "-20" F,
		P "20" F,
		P "100000" F,
		P "-100000" F
		};

	int out_pipe[2];
	int saved_stdout;

	char expected[PF_BUF_SIZE] = {0};
	char actual[PF_BUF_SIZE] = {0};

	int complete_res = 1;

	saved_stdout = dup(STDOUT_FILENO);

	if (pipe(out_pipe) != 0)
	{
		exit(1);
	}

	dup2(out_pipe[1], STDOUT_FILENO);
	close(out_pipe[1]);

	for (int i = 0; i < 12; i++)
	{
		int res = 1;
		sprintf(format_buffer, test_strs[i], format);

		set_signature("printf(%s, 'x')", escape_str(format_buffer));

		int ex_read, act_read;
		int expected_ret = printf((const char *)format_buffer, 'x');
		fflush(stdout);
		write(1, "", 1);
		if ((ex_read = read(out_pipe[0], expected, PF_BUF_SIZE - 1)) == -1)
			exit(-1);

		int actual_ret = ft_printf((const char *)format_buffer, 'x');
		fflush(stdout);
		write(1, "", 1);
		if ((act_read = read(out_pipe[0], actual, PF_BUF_SIZE - 1)) == -1)
			exit(-1);

		res = same_mem(expected, actual, MAX(ex_read, act_read)) && res;
		res = same_value(expected_ret, actual_ret) && res;
		res = check_leaks(NULL) && res;
		show_result(res, "");

		complete_res = complete_res && res;
	}

	dup2(saved_stdout, STDOUT_FILENO);

	return complete_res;
}

int main(int argn, char **argv)
{
	setup_framework(argn, argv);

	TEST("%c format", {
		test_printf('c');
		test_printf('%');
	})
}