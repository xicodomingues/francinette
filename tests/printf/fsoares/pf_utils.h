#include "utils/utils.h"

#define PF_BUF_SIZE 100005
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

#ifdef STRICT_MEM

#define WRITE_CHECK(fn_call)                                                           \
	reset_write_count();                                                               \
	fn_call;                                                                           \
	t_node *w_allocs = get_all_writes();                                               \
	int write_calls = reset_write_count();                                             \
	int w_offset = g_offset;                                                           \
	for (int i = 0; i < write_calls; i++)                                              \
	{                                                                                  \
		w_offset = sprintf(                                                            \
					   signature + g_offset,                                           \
					   ":\n" MAG "write " NC "failed (returned -1) for %ith write:\n", \
					   i + 1) +                                                        \
				   g_offset;                                                           \
		add_trace_to_signature(w_offset, w_allocs, i);                                 \
		set_write_fail(i);                                                             \
		int pf_res = fn_call;                                                          \
		if (pf_res != -1)                                                              \
			result = error("Printf should return -1 if it encounters errors.\n\n");    \
		result = check_leaks(NULL) && result;                                          \
	}                                                                                  \
	free_all_allocs(w_allocs, write_calls);

#define TEST_STRICT(fn_call)                                                      \
	BASE_NULL_CHECK(fn_call, result, {                                            \
		int pf_res = fn_call;                                                     \
		if (pf_res != -1)                                                         \
			result = error("Printf should return -1 if it encounters errors.\n"); \
		result = check_leaks(NULL) && result;                                     \
	})                                                                            \
	WRITE_CHECK(fn_call)                                                          \
	fflush(stdout);                                                               \
	write(1, "", 1);                                                              \
	if ((act_read = read(out_pipe[0], actual, PF_BUF_SIZE)) == -1)                \
	{                                                                             \
		error("Internal problem, please run the tests again");                    \
		exit(-1);                                                                 \
	}

#else
#define TEST_STRICT(fn_call)
#endif

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
		TEST_STRICT(ft_##fn_call);                                             \
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

int		ft_printf(const char *format, ...);

void cout(const char *f, ...);
int show_result(int res, char *prefix);
void pf_setup_framework(int argn, char **argv);

#ifdef STRICT_MEM
int reset_write_count();
void set_write_fail(int n);
t_node *get_all_writes();
#endif