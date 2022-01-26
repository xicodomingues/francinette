
#include "utils.h"

int single_test_strtrim(char *str, char *set, char *expected)
{
	set_sign("ft_strtrim(\"%s\", \"%s\")", str, set);
	check_alloc_str_return(ft_strtrim(str, set), expected);
}

int test_strtrim()
{
	int res = single_test_strtrim("", "", "");
	res = single_test_strtrim("abcd", "", "abcd") && res;
	res = single_test_strtrim("", "cdef", "") && res;
	res = single_test_strtrim(" . abcd", " ", ". abcd") && res;
	res = single_test_strtrim("ab cd  f    ", " ", "ab cd  f") && res;
	res = single_test_strtrim("xxxz  test with x and z and x .  zx  xx z", "z x", "test with x and z and x .") && res;
	return res;
}

int	main()
{
	handle_signals();
	test(strtrim);
}
