
#include "utils.h"

int single_test_strchr(char *str, int ch)
{
	sprintf(signature, "ft_strchr(%p: \"%s\", %i: %s)", str, str, ch, escape_chr(ch));
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
	res = single_test_strchr("teste", 'e' + 256) && res;
	res = single_test_strchr("teste", 1024) && res;

	return res;
}

int	main()
{
	handle_signals();
	test(strchr);
}
