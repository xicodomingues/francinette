
#include "utils.h"

int single_test_strlcpy(char *dest, char *dest_std, char *src, int n)
{
	int result = 1;
	reset(dest, dest_std, MEM_SIZE);

	sprintf(signature, "ft_strlcpy(dest, \"%s\", %i)", src, n);

	int res = ft_strlcpy(dest, src, n);
	int res_std = strlcpy(dest_std, src, n);
	result = same_value(res, res_std);
	return same_mem(dest_std, dest, MEM_SIZE) && result;
}

int test_strlcpy(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	res = single_test_strlcpy(dest, dest_std, "aaa", 0) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 2) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 3) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 4) && res;
	res = single_test_strlcpy(dest, dest_std, "aasdjj;s;sa", 100) && res;
	return res;
}

int	main()
{
	set_sigsev();
	test(strlcpy);
}
