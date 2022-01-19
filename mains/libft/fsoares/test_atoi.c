
#include "utils.h"

int single_test_atoi(char *str)
{
	sprintf(signature, "atoi(\"%s\")", escape_str(str));
	return same_value(ft_atoi(str), atoi(str));
}

int test_atoi(void)
{
	char buffer[200];
	int res = 1;

	res = single_test_atoi(" \t\v\n\r\f123") && res;
	res = single_test_atoi("0") && res;
	res = single_test_atoi("-1000043") && res;
	res = single_test_atoi(
		"+0000000000000000000000000000000000000000000000000000123") && res;
	res = single_test_atoi("    123") && res;
	res = single_test_atoi("--123") && res;
	res = single_test_atoi("-+123") && res;
	res = single_test_atoi("+-123") && res;
	res = single_test_atoi("++123") && res;
	res = single_test_atoi("- 123") && res;
	res = single_test_atoi("+ 123") && res;
	res = single_test_atoi("+\n123") && res;
	res = single_test_atoi("1209") && res;
	res = single_test_atoi("12/3") && res;
	res = single_test_atoi("12;3") && res;
	sprintf(buffer, "%i", INT_MAX);
	res = single_test_atoi(buffer) && res;
	sprintf(buffer, "%i", INT_MIN);
	res = single_test_atoi(buffer) && res;

	return res;
}

int	main()
{
	handle_signals();
	test(atoi);
}
