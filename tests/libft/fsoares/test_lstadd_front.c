#include "list_utils.h"

int test_single_lstadd_front(int test_number, t_list **list, t_list *to_add, t_list **expected)
{
	char *list_str = list_to_str(list);
	char *to_add_str = node_to_str(to_add);
	set_signature_tn(test_number, "ft_lstadd_front(%s, %s)", list_str, to_add_str);
	free(list_str); free(to_add_str);

	ft_lstadd_front(list, to_add);
	int result = same_list(expected, list);

	null_null_check(ft_lstadd_front(list, to_add), result);
	return result;
}

int test_lstadd_front()
{
	int res = test_single_lstadd_front(1,
		create_list(0), lstnew("new head"), create_list(1, "new head"));
	res = test_single_lstadd_front(2,
		create_list(1, "old head"),
		lstnew("new head"),
		create_list(2, "new head", "old head")) && res;
	res = test_single_lstadd_front(3,
		create_list(1, "old head", "tail"),
		*create_list(2, "new head", "lost node"),
		create_list(2, "new head", "old head", "tail")) && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstadd_front);
}
