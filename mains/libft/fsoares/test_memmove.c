
#include "utils.h"

int single_test_memmove(char *dest, char *dest_std, char *src, char *src_std, char *value, int n)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);
	strcpy(src, value);
	strcpy(src_std, value);

	char *r = ft_memmove(dest, src, n);
	char *rs = memmove(dest_std, src_std, n);
	sprintf(function, "ft_memmove(dest: %p, src: %p, %i)", dest, src, 100);
	return (same_ptr(r, dest) && same_mem(rs, r, MEM_SIZE));
}

int test_memmove(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	res = single_test_memmove(dest, dest_std, dest + 2, dest_std + 2, "abcde", 4) && res;
	res = single_test_memmove(dest + 2, dest_std + 2, dest, dest_std, "abcde", 4) && res;
	res = single_test_memmove(dest, dest_std, dest, dest_std, "abcde", 4) && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(memmove);
}
