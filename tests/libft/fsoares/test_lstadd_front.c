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

int test_single_lstadd_front_multiple_ok(
	int test_number, t_list **list, t_list *to_add, t_list **expected, t_list **other_expected
)
{
	char *list_str = list_to_str(list);
	char *to_add_str = list_to_str(&to_add);
	set_signature_tn(test_number, "ft_lstadd_front(%s, %s)", list_str, to_add_str);
	free(list_str); free(to_add_str);

	ft_lstadd_front(list, to_add);
	int result1 = same_list_bool(expected, list);
	int result2 = same_list_bool(other_expected, list);
	int result = result1 || result2;
	if (!result) {
		char *res_list_str = list_to_str(list);
		char *expected_list_str = list_to_str(expected);
		char *other_expected_list_str = list_to_str(other_expected);
		error("different lists\n" YEL "Expected" NC ": %s\n      OR: %s\n" YEL "Result  " NC ": %s\n\n",
			expected_list_str, other_expected_list_str, res_list_str);
		free(res_list_str);
		free(expected_list_str);
		free(other_expected_list_str);
	}

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
	res = test_single_lstadd_front_multiple_ok(3,
		create_list(2, "old head", "tail"),
		*create_list(2, "new head", "lost node"),
		create_list(3, "new head", "old head", "tail"),
		create_list(4, "new head", "lost node", "old head", "tail")
		) && res;
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstadd_front);
}
