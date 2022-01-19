
#include "utils.h"

int single_test_strrchr(char *str, int ch)
{
	sprintf(signature, "ft_strrchr(%p: \"%s\", %i: %s)", str, str, ch, escape_chr(ch));
	char *res = ft_strrchr(str, ch);
	char *res_std = strrchr(str, ch);

	return same_ptr(res, res_std);
}

int test_strrchr(void)
{
	int res = 1;

	res = single_test_strrchr("teste", 'e') && res;
	res = single_test_strrchr("teste", '\0') && res;
	res = single_test_strrchr("xteste", 'x') && res;
	res = single_test_strrchr("teste", 'x') && res;

	res = single_test_strrchr("teste", 1024 + 'e') && res;

	return res;
}

int	main()
{
	handle_signals();
	test(strrchr);
}
