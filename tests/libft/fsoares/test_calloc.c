
#include "my_utils.h"

int test_single_calloc(int test_number, size_t count, size_t size)
{
	set_signature_tn(test_number, "ft_calloc(%zu, %zu)", count, size);

	reset_malloc_mock();
	void *res_calloc = ft_calloc(count, size);
	void *res_std = calloc(count, size);

	int result = check_mem_size(res_calloc, count * size);
	result = same_mem(res_std, res_calloc, count * size) && result;
	result = check_leaks(res_calloc) && result;

	null_check(ft_calloc(count, size), result);
	return result;
}

int test_calloc()
{
	int res = 1;

	res = test_single_calloc(1, 0, 10) && res;
	res = test_single_calloc(2, 10, 0) && res;
	res = test_single_calloc(3, 10, sizeof(long)) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(calloc);
}
