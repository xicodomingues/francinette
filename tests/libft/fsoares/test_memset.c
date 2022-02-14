
#include "my_utils.h"

int single_test_memset(int test_number, char *m, char *ms, int c, int size)
{
	char *res;
	char *res_std;

	reset(m, ms, MEM_SIZE);
	res_std = memset(ms, c, size);
	res = ft_memset(m, c, size);
	set_signature_tn(test_number, "ft_memset(ptr, %i: %s, %i)", c, escape_chr(c), size);
	return (same_return(m, res) && same_mem(res_std, res, MEM_SIZE));
}

int test_memset(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_memset(1, mem, mem_std, 'x', 0) && res;
	res = single_test_memset(2, mem, mem_std, 'g', 12) && res;
	res = single_test_memset(4, mem, mem_std, 300, 12) && res;
	res = single_test_memset(4, mem, mem_std, 257, 19) && res;

	int m2[MEM_SIZE];
	int ms2[MEM_SIZE];

	reset(m2, ms2, MEM_SIZE);
	int *rs = memset(ms2 + 1, 143462, 4);
	int *r = ft_memset(m2 + 1, 143462, 4);

	set_signature_tn(5, "ft_memset(ptr, %i: %s, %i)", 143462, escape_chr((char)143462), 4);
	res = (same_ptr(r, m2 + 1) && same_mem(rs - 1, r - 1, 0x10)) && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(memset);
}
