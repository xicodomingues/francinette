
#include "utils.h"

int test_single_calloc(size_t count, size_t size)
{
	set_sign("ft_calloc(%zu, %zu)", count, size);

	reset_malloc_mock();
	void *p = ft_calloc(count, size);
	void *res_std = calloc(count, size);

	int result = check_mem_size(p, count * size);
	result = same_mem(res_std, p, count * size) && result;
	result = check_leaks(p) && result;

	null_check(ft_calloc(count, size), result);
	return result;
}

int test_calloc()
{
	int res = 1;

	res = test_single_calloc(0, 10) && res;
	res = test_single_calloc(10, 0) && res;
	res = test_single_calloc(10, sizeof(long)) && res;

	return res;
}

int	main()
{
	handle_signals();
	test(calloc);
}
