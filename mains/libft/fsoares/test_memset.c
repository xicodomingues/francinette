
#include "utils.h"

int single_test_memset(char *m, char *ms, int c, int size)
{
	char *res;
	char *res_std;

	reset(m, ms, MEM_SIZE);
	res_std = memset(ms, c, size);
	res = ft_memset(m, c, size);
	sprintf(function, "ft_memset(%p, %i, %i)", m, c, size);
	return (same_return(res, m) && same_mem(res_std, res, MEM_SIZE));
}

int test_memset(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_memset(mem, mem_std, 'x', 0) && res;
	res = single_test_memset(mem, mem_std, 'g', 12) && res;
	res = single_test_memset(mem, mem_std, 300, 12) && res;
	res = single_test_memset(mem, mem_std, 257, 19) && res;

	int m2[MEM_SIZE];
	int ms2[MEM_SIZE];

	reset(m2, ms2, MEM_SIZE);
	int *rs = memset(ms2 + 1, 143562, 4);
	int *r = ft_memset(m2 + 1, 143562, 4);

	sprintf(function, "ft_memset(ptr, %i, %i)", 143562, 4);
	res = (same_ptr(r, m2 + 1) && same_mem(rs - 1, r - 1, 0x10)) && res;
	return res;
}

int	main()
{
	set_sigsev();
	test(memset);
}
