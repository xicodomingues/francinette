
#include "my_utils.h"

int single_test_itoa(int test_number, char *buffer, int n)
{
	set_signature_tn(test_number, "ft_itoa(%i)", n);
	sprintf(buffer, "%i", n);
	check_alloc_str_return(ft_itoa(n), buffer);
}

int test_itoa()
{
	char buffer[100];
	int res = single_test_itoa(1, buffer, 0);
	res = single_test_itoa(2, buffer, 1000034) && res;
	res = single_test_itoa(3, buffer, -10004) && res;
	res = single_test_itoa(4, buffer, INT_MAX) && res;
	res = single_test_itoa(5, buffer, INT_MIN) && res;
	for (int i = 0; i < REPETITIONS && res; i++) {
		int rd = (int)random() - RAND_MAX / 2;
		res = single_test_itoa(6 + i, buffer, rd) && res;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(itoa);
}
