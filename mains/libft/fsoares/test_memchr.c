
#include "utils.h"

int single_test_memchr(char *str, int ch)
{
	sprintf(function, "ft_memchr(%p, %i(%x): %s)", str, ch, ch % 0x100, escape_chr(ch));
	char *res = ft_strchr(str, ch);
	char *res_std = strchr(str, ch);

	int result = same_ptr((void *)res, (void *)res_std);
	if (!result) {
		print_mem_full(str, 0x30);
	}
	return result;
}

int test_memchr(void)
{
	int res = 1;
	char str[100];

	for (int i = 0; i < REPETITIONS && res; i++) {
		res = single_test_memchr(rand_bytes(str, 0x31), rand() % 0x400) && res;
	}
	return res;
}

int	main()
{
	set_sigsev();
	test(memchr);
}
