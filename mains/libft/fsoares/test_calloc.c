
#include "utils.h"

int test_single_calloc(size_t count, size_t size)
{
	sprintf(signature, "ft_calloc(%zu, %zu)", count, size);

	reset_malloc_mock();
	void *p = ft_calloc(count, size);
	void *res_std = calloc(count, size);

	size_t res = get_malloc_size(p);

	int result = 1;
	if (count * size != res)
		result = error("reserved: std: %zu bytes, your: %zu bytes\n", count * size, res);
	if (count * size > 0) {
		result = same_mem(res_std, p, count * size) & result;
	}
	return result;
}

int test_calloc()
{
	int res = 1;

	res = test_single_calloc(0, 10) && res;
	res = test_single_calloc(10, 0) && res;
	res = test_single_calloc(10, sizeof(int)) && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(calloc);
}
