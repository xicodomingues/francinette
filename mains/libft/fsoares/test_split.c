
#include "utils.h"

char **init_str_array(int n, ...)
{
	va_list argp;
	char **result = calloc(n, sizeof(char *));

	va_start(argp, n);
	for (int i = 0; i < n; i++)
		result[i] = va_arg(argp, char *);

	va_end(argp);
	return result;
}

void print_string_arr(char **array)
{
	int i = 0;
	char *res = array[i];
	printf("[");
	while (res != NULL)
	{
		printf("\"%s\", ", res);
		res = array[++i];
	}
	printf(" NULL]");
}

int same_strings(char **expected, char **result)
{
	int i = 0;
	bool same = true;
	while (expected[i] != NULL)
	{
		if (strcmp(expected[i], result[i]) != 0)
			same = false;
		i++;
	}
	same = expected[i] == result[i] && same;

	if (!same)
	{
		error("\n" YEL "Expected: " NC);
		print_string_arr(expected);
		printf("\n" YEL "Returned: " NC);
		print_string_arr(result);
		printf("\n");
	}

	return same;
}

int test_single_split(char *s, char c, char **expected)
{
	set_sign("ft_split(%s, %i:%s)", escape_str(s), c, escape_chr(c));

	char **res = ft_split(s, c);

	int result = 1;
	result = same_strings(expected, res);
	int i = 0;
	while (expected[i] != NULL)
	{
		result = check_mem_size(res[i], strlen(expected[i]) + 1) && result;
		free(res[i]);
		i++;
	}
	result = check_leaks(res) && result;

	null_check(ft_split(s, c), result)
	return result;
}

int test_split()
{
	char **expected = init_str_array(2, "hello!", NULL);
	int res = test_single_split("hello!", ' ', expected);

	res = test_single_split("xxxxxxxxhello!", 'x', expected) && res;
	res = test_single_split("hello!zzzzzzzz", 'z', expected) && res;
	res = test_single_split("\11\11\11\11hello!\11\11\11\11", '\11', expected) && res;

	expected = init_str_array(1, NULL);
	res = test_single_split("", 'a', expected) && res;
	res = test_single_split("ggggggggggg", 'g', expected) && res;

	expected = init_str_array(5, "1", "2a,", "3", "--h", NULL);
	res = test_single_split("^^^1^^2a,^^^^3^^^^--h^^^^", '^', expected) && res;

	return res;
}

int main()
{
	handle_signals();
	test(split);
}
