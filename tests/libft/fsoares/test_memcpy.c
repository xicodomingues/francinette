
#include "my_utils.h"

int single_test_memcpy(int test_number, char *dest, char *dest_std, char *src, char *src_std, int n)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);

	rand_str(src , rand() % 55 + 1);
	memcpy(src_std, src, 100);

	char *res = ft_memcpy(dest, src, n);
	char *res_std = memcpy(dest_std, src_std, n);

	set_signature_tn(test_number, "ft_memcpy(dest, src: %s, n: %i)", escape_str(src), n);
	return (same_return(dest, res) && same_mem(res_std, res, MEM_SIZE));
}

int test_memcpy(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	char src[MEM_SIZE];
	char src_std[MEM_SIZE];

	int res = 1;

	res = single_test_memcpy(1, dest, dest_std, src, src_std, 0);
	for (int n = 0; n < REPETITIONS && res; n++)
		res = single_test_memcpy(2 + n, dest, dest_std, src, src_std, rand() % 70) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(memcpy);
}
