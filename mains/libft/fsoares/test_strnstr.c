
#include "utils.h"

int single_test_strnstr(char *str1, char *str2, size_t n)
{
	sprintf(signature, "ft_strnstr(%p: %s, %s, %lu)", str1, escape_str(str1), escape_str(str2), n);
	char * res = ft_strnstr(str1, str2, n);
	char * res_std = strnstr(str1, str2, n);

	return same_ptr(res, res_std);
}

int test_strnstr(void)
{
	int res = 1;

	char empty[10];

	empty[0] = 0;
	empty[1] = 'a';

	res = single_test_strnstr("abc", "xyz", 0) && res;
	res = single_test_strnstr("abc", "xyz", 1) && res;
	res = single_test_strnstr("", "", 0) && res;
	res = single_test_strnstr("", "", 1) && res;
	res = single_test_strnstr("", "", 2) && res;
	res = single_test_strnstr("", "teste", 0) && res;
	res = single_test_strnstr("", "teste", 1) && res;
	res = single_test_strnstr("", "teste", 2) && res;
	res = single_test_strnstr("teste", "", 0) && res;
	res = single_test_strnstr("teste", "", 1) && res;
	res = single_test_strnstr("teste", "", 2) && res;
	res = single_test_strnstr("abcdefgh", "abc", 2) && res;
	res = single_test_strnstr("abcdefgh", "abc", 3) && res;
	res = single_test_strnstr("abcdefgh", "abc", 4) && res;
	res = single_test_strnstr("abcdefgh", "abc", 5) && res;
	res = single_test_strnstr("abc", "abcdef", 2) && res;
	res = single_test_strnstr("abc", "abcdef", 3) && res;
	res = single_test_strnstr("abc", "abcdef", 4) && res;
	res = single_test_strnstr("abc", "abcdef", 5) && res;
	res = single_test_strnstr("aaxx", "xx", 2) && res;
	res = single_test_strnstr("aaxx", "xx", 3) && res;
	res = single_test_strnstr("aaxx", "xx", 4) && res;
	res = single_test_strnstr("aaxx", "xx", 5) && res;
	res = single_test_strnstr("aaxx", "xx", 6) && res;

	res = single_test_strnstr(empty, "xx", 0xffffffff) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_strnstr((char *)s1, (char *)s2, 3) && res;
	res = single_test_strnstr((char *)s1, (char *)s2, 4) && res;
	res = single_test_strnstr((char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_strnstr((char *)s1, (char *)s2, 7);
	if (!other) {
		printf(LRED "You are not stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	handle_signals();
	test(strnstr);
}
