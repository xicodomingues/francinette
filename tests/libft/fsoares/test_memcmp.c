
#include "utils.h"

int single_test_memcmp(int test_number, char *str1, char *str2, size_t n)
{
	set_signature(test_number, "ft_memcmp(%s, %s, %lu)", escape_str(str1), escape_str(str2), n);
	int res = ft_memcmp(str1, str2, n);
	int res_std = memcmp(str1, str2, n);

	return same_sign(res_std, res);
}

int test_memcmp(void)
{
	int res = 1;

	res = single_test_memcmp(1, "teste", "teste", 0) && res;
	res = single_test_memcmp(2, "teste", "teste", 1) && res;
	res = single_test_memcmp(3, "teste", "teste", 5) && res;
	res = single_test_memcmp(4, "teste", "teste", 6) && res;
	res = single_test_memcmp(5, "teste", "testex", 6) && res;
	res = single_test_memcmp(6, "teste", "test", 10) && res;
	res = single_test_memcmp(7, "test", "teste", 10) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_memcmp(8, (char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_memcmp(9, (char *)s1, (char *)s2, 7);
	if (!other && res) {
		fprintf(errors_file, BRED "You are stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	handle_signals();
	test(memcmp);
}
