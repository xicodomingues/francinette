
#include "my_utils.h"

int single_test_strdup(int test_number, char *str, char *expected)
{
	set_signature_tn(test_number, "ft_strdup(%s)", escape_str(str));
	check_alloc_str_return(ft_strdup(str), expected);
}

int test_strdup()
{
	int res = 1;
	res = single_test_strdup(1, "", "") && res;
	res = single_test_strdup(2, "sadfvbf", "sadfvbf") && res;
	res = single_test_strdup(3, "fdfjkdf\n35346", "fdfjkdf\n35346") && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strdup);
}
