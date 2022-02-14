
#include "my_utils.h"

int single_test_strncmp(int test_number, char *str1, char *str2, size_t n)
{
	set_signature_tn(test_number, "ft_strncmp(%s, %s, %lu)", escape_str(str1), escape_str(str2), n);
	int res = ft_strncmp(str1, str2, n);
	int res_std = strncmp(str1, str2, n);

	return same_sign(res_std, res);
}

int test_strncmp(void)
{
	int res = 1;


	res = single_test_strncmp(1, "", "", 0) && res;
	res = single_test_strncmp(2, "", "", 1) && res;
	res = single_test_strncmp(3, "", "", 2) && res;
	res = single_test_strncmp(4, "test", "", 0) && res;
	res = single_test_strncmp(5, "test", "", 1) && res;
	res = single_test_strncmp(6, "test", "", 2) && res;
	res = single_test_strncmp(7, "", "test", 0) && res;
	res = single_test_strncmp(8, "", "test", 1) && res;
	res = single_test_strncmp(9, "", "test", 2) && res;
	res = single_test_strncmp(10, "teste", "teste", 0) && res;
	res = single_test_strncmp(12, "teste", "teste", 1) && res;
	res = single_test_strncmp(13, "teste", "teste", 5) && res;
	res = single_test_strncmp(14, "teste", "teste", 6) && res;
	res = single_test_strncmp(15, "teste", "teste", 7) && res;
	res = single_test_strncmp(16, "teste", "testex", 6) && res;
	res = single_test_strncmp(17, "teste", "test", 10) && res;
	res = single_test_strncmp(18, "test", "teste", 10) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_strncmp(19, (char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_strncmp(20, (char *)s1, (char *)s2, 7);
	if (!other) {
		fprintf(errors_file, BRED "You are not stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strncmp);
}
