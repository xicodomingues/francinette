
#include "utils.h"

int single_test_strdup(char *str, char *expected)
{
	set_sign("ft_strdup(%s)", escape_str(str));
	check_alloc_str_return(ft_strdup(str), expected);
}

int test_strdup()
{
	int res = 1;
	res = single_test_strdup("", "") && res;
	res = single_test_strdup("sadfvbf", "sadfvbf") && res;
	res = single_test_strdup("fdfjkdf\01235346", "fdfjkdf\01235346") && res;
	return res;
}

int	main()
{
	handle_signals();
	test(strdup);
}
