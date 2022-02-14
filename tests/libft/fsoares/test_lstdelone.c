
#include "list_utils.h"


void free_str(void *str)
{
	free(str);
}

void free_str_ptr(void *str)
{
	free(*((void **)str));
}

int test_lstdelone()
{
	char *elem_str = node_to_str(lstnew("add"));
	set_signature_tn(1, "ft_lstdelone(%s, [(x) => free(x)])", elem_str);
	free(elem_str);

	reset_malloc_mock();
	char *s = malloc(6);
	strcpy(s, "teste");
	t_list *l = lstnew(s);
	ft_lstdelone(l, free_str);
	int res = check_leaks(NULL);
	if (!res)
	{
		fseek(errors_file, -1, SEEK_CUR);
		fprintf(errors_file, "" BMAG "del" NC " should be used on " BLU "content" NC \
				", and " BMAG "free" NC " on the " BLU "lst" NC "\n\n");
	}

	// 2
	char *warn = (NC "Do not use " BMAG "del" NC " on the " BLU "lst" NC ". Use " BMAG "free" NC " instead");
	set_signature_tn(2, "ft_lstdelone({node: content->ptr->\"test\"}, [(x) => free(" RED "*" CYN "x)]): %s", warn);
	reset_malloc_mock();
	s = malloc(5);
	strcpy(s, "test");
	l = lstnew(&s);
	ft_lstdelone(l, free_str_ptr);
	res = check_leaks(NULL) && res;

	// 3
	s = malloc(5);
	strcpy(s, "test");
	t_list **list = create_list(2, s, "second");
	t_list *keep = (*list)->next;
	char *lst_str = list_to_str(list);
	set_signature_tn(3, "ft_lstdelone(%s, [(x) => free(x)]): " NC "The second node should not be freed", lst_str);
	reset_malloc_mock();
	ft_lstdelone(*list, free_str);
	free(keep);
	res = check_leaks(NULL) && res;

	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstdelone);
}
