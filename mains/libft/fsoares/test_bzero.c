
#include "utils.h"

int single_test_bzero(char *m, char *ms, int size)
{
	reset(m, ms, MEM_SIZE);
	bzero(ms, size);
	ft_bzero(m, size);
	sprintf(signature, "ft_bzero(%p, %i)", m, size);
	return (same_mem(ms, m, MEM_SIZE));
}

int test_bzero(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_bzero(mem, mem_std, 0) && res;
	res = single_test_bzero(mem, mem_std, 12) && res;
	res = single_test_bzero(mem + 2, mem_std + 2, 40) && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(bzero);
}
