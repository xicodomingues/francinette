#include "list_utils.h"

int check_allocs(void *content, t_list *expected)
{
	t_list *res = ft_lstnew(content);
	int result = same_list_elem(expected, res);
	result = check_mem_size(res, sizeof(t_list)) && result;
	result = check_leaks(res) && result;
	null_check(ft_lstnew(content), result);
	return result;
}

int test_single_lstnew(char *content, t_list *expected)
{
	set_sign("ft_lstnew(%p: %s)", content, escape_str(content));
	expected->content = content;
	return check_allocs(content, expected);
}

int test_lstnew()
{
	char str[20];
	t_list expected;
	expected.next = NULL;
	int res = test_single_lstnew(NULL, &expected);
	res = test_single_lstnew("hahaha", &expected) && res;
	for (int i = 0; i < REPETITIONS && res; i++)
	{
		sprintf(str, "%i", i);
		res = test_single_lstnew(str, lstnew(str)) && res;
	}
	return res;
}

int main()
{
	handle_signals();
	test(lstnew);
}
