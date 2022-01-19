
#include "utils.h"

int single_test_strdup(char *str)
{
	set_sign("ft_strdup(\"%s\")", escape_str(str));

	char *res_std = strdup(str);
	check_alloc_str_return(ft_strdup(str), res_std);
	free(res_std);
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
