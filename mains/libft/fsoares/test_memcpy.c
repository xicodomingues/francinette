
#include "utils.h"

int single_test_memcpy(char *dest, char *dest_std, char *src, char *src_std)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);

	rand_bytes(src + 6, rand() % 55 + 1);
	memcpy(src_std + 6, src + 6, 100);

	char *res = ft_memcpy(dest, src, 100);
	char *res_std = memcpy(dest_std, src_std, 100);

	sprintf(function, "ft_memcpy(dest: %p, src: %s, n: %i)", 100);
	return (same_return(res, dest) && same_mem(res_std, res, MEM_SIZE));
}

int test_memcpy(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	char src[MEM_SIZE];
	char src_std[MEM_SIZE];

	int res = 1;
	for (int n = 0; n < REPETITIONS && res; n++)
		res = single_test_memcpy(dest, dest_std, src, src_std) && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(memcpy);
}
