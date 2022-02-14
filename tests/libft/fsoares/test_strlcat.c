
#include "my_utils.h"


int single_test_strlcat(int test_number, char *dest, char *dest_std, char *orig, char *src, int n)
{
	int result = 1;

	set_signature_tn(test_number, "ft_strlcat(\"%s\", \"%s\", %i)", orig, src, n);
	reset_with(dest, dest_std, orig, MEM_SIZE);

	int res = ft_strlcat(dest, src, n);
	int res_std = strlcat(dest_std, src, n);
	result = same_value(res_std, res);
	return same_mem(dest_std, dest, (n / 16 + 1) * 16) && result;
}

int test_strlcat(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	for (int i = 0; i < 8; i++)
		res = single_test_strlcat(1 + i, dest, dest_std, "pqrstuvwxyz", "abcd", i) && res;

	res = single_test_strlcat(9, dest, dest_std, "pqrstuvwxyz", "abcd", 20) && res;

	for (int i = 10; i < 18; i++)
		res = single_test_strlcat(i, dest, dest_std, "pqrs", "abcdefghi", i) && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strlcat);
}
