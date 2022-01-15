
#include "utils.h"

int compare_strlen(char *str)
{
	sprintf(function, "ft_strlen(\"%s\")", escape_str(str));
	return same_value(ft_strlen(str), strlen(str));
}

int test_strlen(void)
{
	char str[100];
	int res = 1;

	for (int n = 0; n < REPETITIONS && res; n++)
	{
		rand_bytes(str, rand() % 98 + 1);
		res = compare_strlen(str) && res;
	}
	res = compare_strlen("") && res;
	str[0] = EOF;
	str[1] = '\0';
	res = compare_strlen(str) && res;
	return res;
}

int	main()
{
	set_sigsev();
	test(strlen);
}
