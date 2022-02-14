
#include "my_utils.h"

int single_test_strmapi(int test_number, char *str, char (*fn)(unsigned int, char), char *func, char *expected)
{
	set_signature_tn(test_number, "ft_strmapi(\"%s\", %s)", str, func);
	check_alloc_str_return(ft_strmapi(str, fn), expected);
}

char add(unsigned int i, char c) {
	return (char)(i + c);
}

char to_char_zero(unsigned int i, char c) {
	c = (char)i;
	return '0' + c - c;
}

int test_strmapi()
{
	int res = single_test_strmapi(1, "", add, "{(i, c) => i + c}", "");
	res = single_test_strmapi(2, "abcd0 ", add, "{(i, c) => i + c}", "aceg4%") && res;
	res = single_test_strmapi(3, "abcdfsdfs", to_char_zero, "{(i, c) => '0'}", "000000000") && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strmapi);
}
