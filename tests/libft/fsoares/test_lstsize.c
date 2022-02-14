
#include "list_utils.h"

int single_test_lstsize(int test_number, t_list **list, int expected)
{
	char *list_str = list_to_str(list);
	set_signature_tn(test_number, "ft_lstsize(%s)", list_str);
	free(list_str);

	int result = same_value(expected, ft_lstsize(*list));
	null_null_check(ft_lstsize(*list), result);
	return result;
}

int test_lstsize()
{
	int res = single_test_lstsize(1, create_list(0), 0);
	res = single_test_lstsize(2, create_list(1, "one"), 1) && res;
	res = single_test_lstsize(3,
		create_list(5, "one", "two", "three", "four", "five"),
		5) && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstsize);
}
