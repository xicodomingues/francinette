
#include "utils.h"

int single_test_memmove(char *dest, char *dest_std, char *src, char *src_std, char *value, int n)
{
	reset(dest, dest_std, MEM_SIZE + 10);
	reset(src, src_std, MEM_SIZE + 10);
	strcpy(src, value);
	strcpy(src_std, value);

	char *r = ft_memmove(dest, src, n);
	char *rs = memmove(dest_std, src_std, n);
	sprintf(signature, "ft_memmove(%p: \"%s\", %p: \"%s\", %i)", dest, dest, src, src, n);
	return (same_return(r, dest) && same_mem(rs, r, MEM_SIZE));
}

int test_memmove(void)
{
	char dest[MEM_SIZE + 10];
	char dest_std[MEM_SIZE + 10];

	int res = 1;
	res = single_test_memmove(dest, dest_std, dest + 2, dest_std + 2, "123456", 4) && res;
	res = single_test_memmove(dest + 2, dest_std + 2, dest, dest_std, "123456", 4) && res;
	res = single_test_memmove(dest, dest_std, dest, dest_std, "123456", 4) && res;
	res = single_test_memmove(dest + 2, dest_std + 2, dest, dest_std, "123456", 0) && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(memmove);
}
