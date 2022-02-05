
#include "utils.h"

#include "utils.h"

int test_single_strjoin(int test_number, char *str1, char *str2, char *expected)
{
	set_signature(test_number, "ft_strjoin(\"%s\", \"%s\")", str1, str2);
	check_alloc_str_return(ft_strjoin(str1, str2), expected);
}

int test_strjoin()
{
	int res = 1;
	res = test_single_strjoin(1, "", "", "") && res;
	res = test_single_strjoin(2, "abc", "", "abc") && res;
	res = test_single_strjoin(3, "", "abc", "abc") && res;
	res = test_single_strjoin(4, "abcd", "efghi", "abcdefghi") && res;

	return res;
}

int	main()
{
	handle_signals();
	test(strjoin);
}
