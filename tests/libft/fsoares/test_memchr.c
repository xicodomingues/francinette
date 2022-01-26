
#include "utils.h"

int single_test_memchr(char *str, int ch, size_t n)
{
	sprintf(signature, "ft_memchr(%p, %i(%x): %s, %zu)", str, ch, ch % 0x100, escape_chr(ch), n);
	char *res = ft_memchr(str, ch, n);
	char *res_std = memchr(str, ch, n);

	int result = same_ptr((void *)res, (void *)res_std);
	if (!result) {
		print_mem_full(str, 0x30);
	}
	return result;
}

int test_memchr(void)
{
	int res = 1;
	char str[MEM_SIZE];

	for (int i = 0; i < REPETITIONS && res; i++) {
		res = single_test_memchr(rand_bytes(str, 0x31), rand() % 0x400, rand() % 0x30) && res;
	}
	single_test_memchr(rand_bytes(str, 0x31), 123, 0);
	return res;
}

int	main()
{
	handle_signals();
	test(memchr);
}
