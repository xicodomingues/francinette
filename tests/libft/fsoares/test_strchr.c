
#include "my_utils.h"

int single_test_strchr(int test_number, char *str, int ch)
{
	set_signature_tn(test_number, "ft_strchr(%p: \"%s\", %i: %s)", str, str, ch, escape_chr(ch));
	char *res = ft_strchr(str, ch);
	char *res_std = strchr(str, ch);

	return same_offset(str, res_std, str, res);
}

int test_strchr(void)
{
	int res = 1;

	res = single_test_strchr(1,"teste", 't') && res;
	res = single_test_strchr(2,"teste", 'e') && res;
	res = single_test_strchr(3, "teste", '\0') && res;
	res = single_test_strchr(4, "teste", 'a') && res;
	res = single_test_strchr(5, "teste", 'e' + 256) && res;
	res = single_test_strchr(6, "teste", 1024) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(strchr);
}
