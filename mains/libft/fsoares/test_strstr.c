
#include "utils.h"

int single_test_strchr(char *str, int ch)
{
	sprintf(function, "ft_strchr(%p: \"%s\", %s)", str, str, escape_chr(ch));
	char *res = ft_strchr(str, ch);
	char *res_std = strchr(str, ch);

	return same_ptr(res, res_std);
}

int test_strchr(void)
{
	int res = 1;

	res = single_test_strchr("teste", 't') && res;
	res = single_test_strchr("teste", 'e') && res;
	res = single_test_strchr("teste", '\0') && res;
	res = single_test_strchr("teste", 'a') && res;

	return res;
}

int	main()
{
	set_sigsev();
	test(strstr);
}
