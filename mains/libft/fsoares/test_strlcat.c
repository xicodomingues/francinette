
#include "utils.h"


int single_test_strlcat(char *dest, char *dest_std, char *orig, char *src, int n)
{
	int result = 1;

	sprintf(function, "ft_strlcat(\"%s\", \"%s\", %i)", orig, src, n);
	reset_with(dest, dest_std, orig, MEM_SIZE);

	int res = ft_strlcat(dest, src, n);
	int res_std = strlcat(dest_std, src, n);
	result = same_value(res, res_std);
	return same_mem(dest_std, dest, MEM_SIZE) && result;
}

int test_strlcat(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 0) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 1) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 2) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 3) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 4) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 5) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 6) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 7) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 20) && res;
	res = single_test_strlcat(dest, dest_std, "pqrs", "abcdefghi", 20) && res;
	return res;
}

int	main()
{
	set_sigsev();
	test(strlcat);
}
