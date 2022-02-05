#include "utils.h"
#include "../../get_next_line.h"

int check_res(int res, char *prefix)
{
	if (!res)
		printf(RED "%i.%sKO " NC, ++g_test, prefix);
	else
		printf(GRN "%i.%sOK " NC, ++g_test, prefix);
	fflush(stdout);
	return res;
}

int leak_check()
{
	int res = 1;
	res = check_leaks(NULL);
	check_res(res, "LEAKS_");
	return res;
}

int test_gnl_func(int fd, char *expected, char *input)
{
	set_signature("get_next_line(%i: %s)", fd, escape_str(input));

	char *next = get_next_line(fd);
	int res = same_string(expected, next);
	if (expected != NULL) {
		res = check_mem_size(next, strlen(expected) + 1);
		if (!res)
			fprintf(errors_file, "should reserve space for the string: %s\n", escape_str(expected));
	}
	check_res(res, "");
	free(next);
	return res;
}

int null_check_gnl(char *file)
{
#ifdef STRICT_MEM
	printf("NULL_CHECK: ");
	fflush(stdout);
	int fd = open(file, O_RDONLY);
	int lines = 0;
	reset_malloc_mock();
	char *res;
	do {
		res = get_next_line(fd);
		lines++;
	}
	while (res != NULL);
	close(fd);
	int result = 1;
	int total = reset_malloc_mock();
	for (int i = 0; i < total; i++) {
		sprintf(signature + g_offset, NC " NULL check for %ith malloc", i + 1);
		malloc_set_null(i);
		int count = 0;

		int fd = open(file, O_RDONLY);
		do {
			res = get_next_line(fd);
			free(res);
			if (res != NULL)
				count++;
		}
		while (res != NULL);
		close(fd);

		result = check_leaks(NULL) && result;
		if (lines == count)
			result = error("Should exit early and return NULL\n");
	}
	if (result)
		printf(GRN "OK" NC);
	else
		printf(BRED "KO" NC);
	return result;
#else
	(void)file;
	return 1;
#endif
}