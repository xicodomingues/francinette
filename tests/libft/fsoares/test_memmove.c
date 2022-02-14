
#include "my_utils.h"

int single_test_memmove(int test_number, char *dest, char *dest_std, char *src, char *src_std, char *value, int n)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);
	strcpy(src, value);
	strcpy(src_std, value);

	set_signature_tn(test_number, "ft_memmove(%p, %p: \"%s\", %i)", dest, src, src, n);

	char *result = ft_memmove(dest, src, n);
	char *expected = memmove(dest_std, src_std, n);
	return (same_return(dest, result) && same_mem(expected, result, MEM_SIZE));
}

int test_memmove(void)
{
	char dest[MEM_SIZE + 10];
	char dest_std[MEM_SIZE + 10];

	int res = 1;
	res = single_test_memmove(1, dest, dest_std, dest + 2, dest_std + 2, "123456", 4) && res;
	res = single_test_memmove(2, dest + 2, dest_std + 2, dest, dest_std, "123456", 4) && res;
	res = single_test_memmove(3, dest, dest_std, dest, dest_std, "123456", 4) && res;
	res = single_test_memmove(4, dest + 2, dest_std + 2, dest, dest_std, "123456", 0) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(memmove);
}
