#define _GNU_SOURCE
#include <unistd.h>

#include "file_utils.h"
#include "../get_next_line.h"

int next_read_error = 0;

ssize_t read(int fildes, void *buf, size_t nbyte)
{
	ssize_t(*libc_read)(int, void *, size_t) =
		(ssize_t (*)(int, void *, size_t))dlsym(RTLD_NEXT, "read");
	if (nbyte != BUFFER_SIZE && nbyte != 0) {
		fprintf(errors_file, "Please use the read size provided by the compile variable BUFFER_SIZE: %i\n", BUFFER_SIZE);
		printf(RED "Use the BUFFER_SIZE (%i) on the read calls, instead of what you wanted to read (%zi).\n" NC, BUFFER_SIZE, nbyte);
		exit(1);
	}
	if (next_read_error) {
		next_read_error = 0;
		return -1;
	}
	return libc_read(fildes, buf, nbyte);
}

/**
 * Will return zero if there are leaks, 1 if there are no leaks
 */
int leak_check()
{
	int res = 1;
	res = check_leaks(NULL);
	show_res(res, "_LEAKS");
	return res;
}

int test_gnl_func(int fd, char *expected, char *input)
{
	set_signature("get_next_line(%i: %s)", fd, escape_str(input));

	char *next = get_next_line(fd);
	int res = same_string(expected, next);
	if (expected != NULL)
	{
		int mem_res = check_mem_size(next, strlen(expected) + 1);
		if (!mem_res)
			fprintf(errors_file, "should reserve space for the string: %s\n", escape_str(expected));
		res = mem_res && res;
	}
	show_res(res, "");
	free(next);
	return res;
}

void print_file_content(char * content) {
	int line = 1;
	fprintf(errors_file, NC "1: " GRN);
	while (*content)
	{
		if (*content == '\n')
			fprintf(errors_file, "\\n");
		fprintf(errors_file, "%c", *content);
		if (*content == '\n')
			fprintf(errors_file, NC "%i: " GRN, ++line);
		content++;
	}
	fprintf(errors_file, NC);
}

int test_gnl_func_limits(int fd, char *expected, int line, char *content, char *input)
{
	set_signature("get_next_line(%i: %s)", fd, escape_str(input));

	char *next = get_next_line(fd);
	int res = same_string(expected, next);
	if (!res) {
		fprintf(errors_file, "asking for line: %i of file:\n", line + 1);
		print_file_content(content);
		fprintf(errors_file, "\n\n");
	}
	if (expected != NULL)
	{
		int mem_res = check_mem_size(next, strlen(expected) + 1);
		if (!mem_res)
			fprintf(errors_file, "should reserve space for the string: %s\n", escape_str(expected));
		res = mem_res && res;
	}
	show_res(res, "");
	free(next);
	return res;
}

int silent_gnl_test(int fd, char *expected)
{
	set_signature("get_next_line(%i: \"lines_around_10.txt\")", fd);

	char *next = get_next_line(fd);
	int res = same_string(expected, next);
	if (!res)
	{
		printf("expected: --%s--, result: --%s--\n", expected, next);
		printf(RED "%i.KO " NC, g_test++);
	}
	free(next);
	return res;
}

int null_check_gnl(char *file)
{
#ifdef STRICT_MEM
	int fd = open(file, O_RDONLY);
	int lines = 0;
	reset_malloc_mock();
	char *res;
	do
	{
		res = get_next_line(fd);
		lines++;
	} while (res != NULL && lines < 20);
	close(fd);
	int result = 1;
	t_node *allocs = get_all_allocs();
	int total = reset_malloc_mock();
	int offset = g_offset;
	for (int i = 0; i < total; i++)
	{
		offset = sprintf(
					 signature + g_offset,
					 ":\n" MAG "malloc " NC "protection check for %ith malloc:\n",
					 i + 1) +
				 g_offset;
		add_trace_to_signature(offset, allocs, i);
		malloc_set_null(i);

		int count = 0;
		int fd = open(file, O_RDONLY);
		do
		{
			res = get_next_line(fd);
			free(res);
			if (res != NULL)
				count++;
		} while (res != NULL && count < 20);
		close(fd);
		result = check_leaks(NULL) && result;
		do
		{
			res = get_next_line(fd);
		} while (res != NULL);
		if (lines == count)
			result = error("Should exit early and return NULL\n");
	}
	show_res(result, "_NULL_CHECK");
	return result;
#else
	(void)file;
	return 1;
#endif
}