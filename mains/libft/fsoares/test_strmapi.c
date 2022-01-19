
#include "utils.h"

int single_test_strmapi(char *str, char(*fn)(unsigned int, char), char *func, char *expected)
{
	set_sign("ft_strmapi(\"%s\", %s)", str, func);
	check_alloc_str_return(ft_strmapi(str, fn), expected);
}

char add(unsigned int i, char c) {
	return (char)(i + c);
}

char to_char_zero(unsigned int i, char c) {
	c = (char)i;
	return '0';
}

int test_strmapi()
{
	int res = single_test_strmapi("", add, "{(i, c) => i + c}", "");
	res = single_test_strmapi("abcd0 ", add, "{(i, c) => i + c}", "aceg4%") && res;
	res = single_test_strmapi("abcdfsdfs", to_char_zero, "{(i, c) => i + c}", "000000000") && res;

	return res;
}

int	main()
{
	handle_signals();
	test(strmapi);
}
