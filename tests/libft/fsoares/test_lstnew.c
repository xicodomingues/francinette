#include "list_utils.h"

int check_allocs(void *content, t_list *expected)
{
	t_list *res = ft_lstnew(content);
	int result = same_list_elem(expected, res);
	if (!result){
		fprintf(errors_file, "Check that you are setting " MAG "new_node->next" NC " to NULL\n\n");
	}
	result = check_mem_size(res, sizeof(t_list)) && result;
	result = check_leaks(res) && result;
	null_check(ft_lstnew(content), result);
	return result;
}

int test_single_lstnew(int test_number, char *content, t_list *expected)
{
	set_signature_tn(test_number, "ft_lstnew(%p: %s)", content, escape_str(content));
	expected->content = content;
	return check_allocs(content, expected);
}

int test_lstnew()
{
	t_list expected;
	expected.next = NULL;
	int res = test_single_lstnew(1, NULL, &expected);
	res = test_single_lstnew(2, "hahaha", &expected) && res;
	return res;
}

int main()
{
	handle_signals_with_time();
	test(lstnew);
}
