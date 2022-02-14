
#include "list_utils.h"

void count_chars(void *s)
{
	char *str = (char *)s;
	sprintf(str, "%zu", strlen(str));
}

int single_test_lstiter(int test_number, t_list **initial, t_list ** expected)
{
	char *l_str = list_to_str(initial);
	set_signature_tn(test_number, "ft_lstiter(%s, [(s) => (s = strlen(s))])", l_str); free(l_str);
	ft_lstiter(*initial, count_chars);
	int res = same_list(expected, initial);

	null_null_check(ft_lstiter(*initial, count_chars), res);
	return res;
}

int test_lstiter()
{
	int res = single_test_lstiter(1, create_list(0), create_list(0));
	res = single_test_lstiter(2, create_list(1, strdup("one")), create_list(1, "3")) && res;
	res = single_test_lstiter(3,
		create_list(5, strdup("um"), strdup("dois"), strdup("tres"), strdup("quatro"), strdup("cinco")),
		create_list(5, "2", "4", "4", "6", "5")) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstiter);
}
