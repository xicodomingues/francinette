
#include "utils.h"

int single_test_strdup(char *str)
{
	set_sign("ft_strdup(\"%s\")", escape_str(str));

	char *res = ft_strdup(str);
	char *res_std = strdup(str);

	int result = check_mem_size(res, strlen(str) + 1);
	result = same_mem(res, res_std, strlen(str) + 1) && result;

	free(res_std);
	result = check_leaks(res) && result;

	null_check(ft_strdup(str), result);
	return result;
}

int test_strdup()
{
	int res = 1;
	res = single_test_strdup("") && res;
	res = single_test_strdup("sadfvbf") && res;
	res = single_test_strdup("fdfjkdf\01235346") && res;
	return res;
}

int	main()
{
	handle_signals();
	test(strdup);
}
