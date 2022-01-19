
#include "utils.h"

#include "utils.h"

int test_single_strjoin(char *str1, char *str2, char *expected)
{
	set_sign("ft_strjoin(\"%s\", \"%s\")", str1, str2);

	char *res = ft_strjoin(str1, str2);

	int result = same_string(expected, res);
	result = check_mem_size(res, strlen(expected) + 1);
	result = check_leaks(res) && result;

	null_check(ft_strjoin(str1, str2), result);
	return result;
}

int test_strjoin()
{
	int res = 1;
	res = test_single_strjoin("", "", "") && res;
	res = test_single_strjoin("abc", "", "abc") && res;
	res = test_single_strjoin("", "abc", "abc") && res;
	res = test_single_strjoin("abcd", "efghi", "abcdefghi") && res;

	return res;
}

int	main()
{
	handle_signals();
	test(strjoin);
}
