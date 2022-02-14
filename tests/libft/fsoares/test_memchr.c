
#include "my_utils.h"

int single_test_memchr(int test_number, char *str, int ch, size_t n)
{
	set_signature_tn(test_number, "ft_memchr(%p, %i(%x): %s, %zu)", str, ch, ch % 0x100, escape_chr(ch), n);
	char *res = ft_memchr(str, ch, n);
	char *res_std = memchr(str, ch, n);

	int result = same_offset(str, res_std, str, res);
	if (!result) {
		fprintf(errors_file, YEL "Memory content:\n" NC);
		print_mem_full(str, 0x30);
		fprintf(errors_file, "\n");
	}
	return result;
}

int test_memchr(void)
{
	int res = 1;
	char str[MEM_SIZE];

	single_test_memchr(1, rand_bytes(str, 0x31), 123, 0);
	for (int i = 0; i < REPETITIONS && res; i++) {
		res = single_test_memchr(2 + i, rand_bytes(str, 0x31), rand() % 0x400, rand() % 0x30) && res;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(memchr);
}
