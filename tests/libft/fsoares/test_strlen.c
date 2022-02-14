
#include "my_utils.h"

int compare_strlen(int test_number, char *str)
{
	set_signature_tn(test_number, "ft_strlen(%s)", escape_str(str));
	return same_value(strlen(str), ft_strlen(str));
}

int test_strlen(void)
{
	char str[100];
	int res = 1;

	res = compare_strlen(1, "") && res;
	str[0] = EOF;
	str[1] = '\0';
	res = compare_strlen(2, str) && res;
	const char *s = "aaaaa";
	ft_strlen(s);

	for (int n = 0; n < REPETITIONS && res; n++)
	{
		rand_str(str, rand() % 98 + 1);
		res = compare_strlen(3 + n, str) && res;
	}
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strlen);
}
