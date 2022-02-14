
#include "my_utils.h"

int single_test_bzero(int test_number, char *res, char *expected, int size)
{
	set_signature_tn(test_number, "ft_bzero(%p, %i)", res, size);
	reset(res, expected, MEM_SIZE);
	bzero(expected, size);
	ft_bzero(res, size);

	return (same_mem(expected, res, MEM_SIZE));
}

int test_bzero(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_bzero(1, mem, mem_std, 0) && res;
	res = single_test_bzero(2, mem, mem_std, 12) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(bzero);
}
