
#include "list_utils.h"

int single_test_lstlast(t_list **list, t_list *expected)
{
	char *list_str = list_to_str(list);
	set_sign("ft_lstlast(%s)", list_str);
	free(list_str);

	int result = same_list_elem(ft_lstlast(*list), expected);
	null_null_check(ft_lstlast(*list), result);
	return result;
}

int test_lstlast()
{
	int res = single_test_lstlast(create_list(0), NULL);
	res = single_test_lstlast(create_list(1, "one"), lstnew("one")) && res;
	res = single_test_lstlast(
		create_list(5, "one", "two", "three", "four", "five"),
		lstnew("five")) && res;
	return res;
}

int	main()
{
	handle_signals();
	test(lstlast);
}
