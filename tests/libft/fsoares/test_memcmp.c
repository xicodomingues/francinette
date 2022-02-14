
#include "my_utils.h"

int single_test_memcmp(int test_number, char *str1, char *str2, size_t n)
{
	set_signature_tn(test_number, "ft_memcmp(%s, %s, %lu)", escape_str(str1), escape_str(str2), n);
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

	char s1[20] = "teste";
	char s2[20] = "test";
	res = single_test_memcmp(6, s1, s2, 10) && res;
	res = single_test_memcmp(7, s2, s1, 10) && res;

	strcpy(s1, "abcdef");
	strcpy(s2, "abc\xfdxx");
	res = single_test_memcmp(8, s1, s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_memcmp(9, s1, s2, 7);
	if (!other && res) {
		fprintf(errors_file, BRED "You are stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(memcmp);
}
