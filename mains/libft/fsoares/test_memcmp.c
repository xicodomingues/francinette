
#include "utils.h"

int single_test_memcmp(char *str1, char *str2, size_t n)
{
	sprintf(signature, "ft_memcmp(\"%s\", \"%s\", %lu)", escape_str(str1), escape_str(str2), n);
	int res = ft_memcmp(str1, str2, n);
	int res_std = memcmp(str1, str2, n);

	return same_sign(res, res_std);
}

int test_memcmp(void)
{
	int res = 1;

	res = single_test_memcmp("teste", "teste", 0) && res;
	res = single_test_memcmp("teste", "teste", 1) && res;
	res = single_test_memcmp("teste", "teste", 5) && res;
	res = single_test_memcmp("teste", "teste", 6) && res;
	res = single_test_memcmp("teste", "testex", 6) && res;
	res = single_test_memcmp("teste", "test", 10) && res;
	res = single_test_memcmp("test", "teste", 10) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_memcmp((char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_memcmp((char *)s1, (char *)s2, 7);
	if (!other) {
		printf(RED "You are stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	set_sigsev();
	test(memcmp);
}
