
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
		char *content = *((char **)node->content);
		sprintf(res, "{node: %p -> %s}", node->content, escape_str(content));
	}
	return res;
}


int test_single_lstclear(t_list **list)
{
	t_list *to_func = NULL;
	char *args[10];
	int i = 0;
	while (*list != NULL)
	{
		args[i] = my_strdup((*list)->content);
		lstadd_back(&to_func, lstnew(args + i));
		*list = (*list)->next;
		i++;
	}

	char *s = list_to_str_fn(&to_func, node_ptr_to_str);
	set_sign("ft_lstclear(%s, [(x) => free(" RED "*" CYN "x)])", s); free(s);

	ft_lstclear(&to_func, free_str_ptr);
	check_leaks(NULL);
	if (*list != NULL)
		return error("The value stored in the lst should be NULL after the clear.\n");
	return 1;
}

int test_lstclear()
{
	int res = test_single_lstclear(create_list(0));
	res = test_single_lstclear(create_list(1, "hello!")) && res;
	res = test_single_lstclear(
		create_list(5, "um", "dois", "tres", "quatro", "cinco")) && res;

	return res;
}

int	main()
{
	handle_signals();
	test(lstclear);
}
