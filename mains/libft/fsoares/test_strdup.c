
#include "utils.h"

int single_test_strdup(char *str)
{
	sprintf(signature, "ft_strdup(\"%s\")", escape_str(str));
	reset_malloc_mock();

	char *res = ft_strdup(str);
	char *res_std = strdup(str);

	int result = 1;
	size_t reserved = get_malloc_size(res);
	size_t expected = strlen(str) + 1;
	if (reserved < strlen(str) + 1)
		result = error("not enough memory allocated, needed: %zu, reserved: %zu\n", expected, reserved);
	return same_mem(res, res_std, strlen(str) + 1) && result;
}

int test_strdup()
{
	int res = 1;
	res = single_test_strdup("") && res;
	res = single_test_strdup("sadfvbf") && res;
	res = single_test_strdup("fdfjkdf\01235346") && res;

	sprintf(signature, CYN "ft_strdup(\"aaa\")" NC " when out of memory should return 'NULL'");
	reset_malloc_mock();
	malloc_set_result(NULL);

	char *str = ft_strdup("aaa");
	if (str != NULL)
		res = error(RED "KO\n");
	return res;
}

int	main()
{
	set_sigsev();
	test(strdup);
}
