
#include "my_utils.h"

int single_test_strnstr(int test_number, char *str1, char *str2, size_t n)
{
	set_signature_tn(test_number, "ft_strnstr(%p: %s, %s, %lu)", str1, escape_str(str1), escape_str(str2), n);
	char * res = ft_strnstr(str1, str2, n);
	char * res_std = strnstr(str1, str2, n);

	return same_offset(str1, res_std, str1, res);
}

int test_strnstr(void)
{
	int res = 1;

	char empty[10];

	empty[0] = 0;
	empty[1] = 'a';

	res = single_test_strnstr(1, "abc", "xyz", 0) && res;
	res = single_test_strnstr(2, "abc", "xyz", 1) && res;
	res = single_test_strnstr(3, "", "", 0) && res;
	res = single_test_strnstr(4, "", "", 1) && res;
	res = single_test_strnstr(5, "", "", 2) && res;
	res = single_test_strnstr(6, "", "teste", 0) && res;
	res = single_test_strnstr(7, "", "teste", 1) && res;
	res = single_test_strnstr(8, "", "teste", 2) && res;
	res = single_test_strnstr(9, "teste", "", 0) && res;
	res = single_test_strnstr(10, "teste", "", 1) && res;
	res = single_test_strnstr(11, "teste", "", 2) && res;
	res = single_test_strnstr(12, "abcdefgh", "abc", 2) && res;
	res = single_test_strnstr(13, "abcdefgh", "abc", 3) && res;
	res = single_test_strnstr(14, "abcdefgh", "abc", 4) && res;
	res = single_test_strnstr(15, "abcdefgh", "abc", 5) && res;
	res = single_test_strnstr(16, "abc", "abcdef", 2) && res;
	res = single_test_strnstr(17, "abc", "abcdef", 3) && res;
	res = single_test_strnstr(18, "abc", "abcdef", 4) && res;
	res = single_test_strnstr(19, "abc", "abcdef", 5) && res;
	res = single_test_strnstr(20, "aaxx", "xx", 2) && res;
	res = single_test_strnstr(21, "aaxx", "xx", 3) && res;
	res = single_test_strnstr(22, "aaxx", "xx", 4) && res;
	res = single_test_strnstr(23, "aaxx", "xx", 5) && res;
	res = single_test_strnstr(24, "aaxx", "xx", 6) && res;

	res = single_test_strnstr(25, empty, "xx", 0xffffffff) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_strnstr(26, (char *)s1, (char *)s2, 3) && res;
	res = single_test_strnstr(27, (char *)s1, (char *)s2, 4) && res;
	res = single_test_strnstr(28, (char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_strnstr(29, (char *)s1, (char *)s2, 7);
	if (!other) {
		fprintf(errors_file, BRED "You are not stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strnstr);
}
