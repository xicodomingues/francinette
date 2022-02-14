
#include "list_utils.h"

void free_str_ptr(void *str)
{
	free(*((void **)str));
}

char *node_ptr_to_str(t_list *node)
{
	char *res = malloc(1000);
	if (node == NULL)
		sprintf(res, "(null)");
	else {
		sprintf(res, "{node: ptr-> %s}", escape_str((char *)node->content));
	}
	return res;
}


int test_single_lstclear(int test_number, t_list **list)
{
	t_list *to_func = NULL;
	char *args[10];
	int i = 0;

	char *s = list_to_str_fn(list, node_ptr_to_str);
	set_signature_tn(test_number, "ft_lstclear(%s, [(x) => free(" RED "*" CYN "x)])", s); free(s);

	while (*list != NULL)
	{
		args[i] = my_strdup((*list)->content);
		lstadd_back(&to_func, lstnew(args + i));
		*list = (*list)->next;
		i++;
	}

	ft_lstclear(&to_func, free_str_ptr);
	int res = check_leaks(NULL);
	if (to_func != NULL)
		return error("The value stored in the lst should be NULL after the clear.\n");
	return res;
}

int test_lstclear()
{
	int res = test_single_lstclear(1, create_list(0));
	res = test_single_lstclear(2, create_list(1, "hello!")) && res;
	res = test_single_lstclear(3,
		create_list(5, "um", "dois", "tres", "quatro", "cinco")) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstclear);
}
