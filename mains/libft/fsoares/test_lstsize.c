
#include "list_utils.h"

int single_test_lstsize(t_list **list, int expected)
{
	char *list_str = list_to_str(list);
	set_sign("ft_lstsize(%s)", list_str);
	free(list_str);

	int result = same_value(ft_lstsize(*list), expected);
	null_null_check(ft_lstsize(*list), result);
	return result;
}

int test_lstsize()
{
	int res = single_test_lstsize(create_list(0), 0);
	res = single_test_lstsize(create_list(1, "one"), 1) && res;
	res = single_test_lstsize(
		create_list(5, "one", "two", "three", "four", "five"),
		5) && res;
	return res;
}

int	main()
{
	handle_signals();
	test(lstsize);
}
