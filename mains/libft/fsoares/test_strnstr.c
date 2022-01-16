
#include "utils.h"

int single_test_strnstr(char *str1, char *str2, size_t n)
{
	sprintf(function, "ft_strnstr(\"%s\", \"%s\", %lu)", escape_str(str1), escape_str(str2), n);
	char * res = ft_strnstr(str1, str2, n);
	char * res_std = strnstr(str1, str2, n);

	return same_ptr(res, res_std);
}

int test_strnstr(void)
{
	int res = 1;

	res = single_test_strnstr("abc", "xyz", 0) && res;
	res = single_test_strnstr("", "", 0) && res;
	res = single_test_strnstr("", "", 1) && res;
	res = single_test_strnstr("abcde", "def", 2) && res;
	res = single_test_strnstr("abcde", "def", 3) && res;
	res = single_test_strnstr("abc", "abcd", 3) && res;
	res = single_test_strnstr("abc", "abcd", 4) && res;
	res = single_test_strnstr("", "teste", 0) && res;
	res = single_test_strnstr("", "teste", 1) && res;
	res = single_test_strnstr("teste", "", 0) && res;
	res = single_test_strnstr("teste", "", 1) && res;
	res = single_test_strnstr("teste", "teste", 7) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_strnstr((char *)s1, (char *)s2, 3) && res;
	res = single_test_strnstr((char *)s1, (char *)s2, 4) && res;
	res = single_test_strnstr((char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_strnstr((char *)s1, (char *)s2, 7);
	if (!other) {
		printf(RED "You are not stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	set_sigsev();
	test(strnstr);
}
