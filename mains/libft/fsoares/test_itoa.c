
#include "utils.h"

int single_test_itoa(char *buffer, int n)
{
	set_sign("ft_itoa(%i)", n);
	sprintf(buffer, "%i", n);
	check_alloc_str_return(ft_itoa(n), buffer);
}

int test_itoa()
{
	char buffer[100];
	int res = single_test_itoa(buffer, 0);
	res = single_test_itoa(buffer, 1000034) && res;
	res = single_test_itoa(buffer, -10004) && res;
	res = single_test_itoa(buffer, INT_MAX) && res;
	res = single_test_itoa(buffer, INT_MIN) && res;
	for (int i = 0; i < REPETITIONS && res; i++) {
		int rd = (int)random() - RAND_MAX / 2;
		res = single_test_itoa(buffer, rd) && res;
	}
	return res;
}

int	main()
{
	handle_signals();
	test(itoa);
}
