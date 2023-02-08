
#include "list_utils.h"

void *map_length(void *s)
{
	char *str = malloc(30);
	if (str != NULL)
		sprintf(str, "__%lX", strlen((char *)s));
	return str;
}

void delete(void *content)
{
	char *str = (char *)content;
	if (str == NULL)
		return;
	if (str[0] != '_' || str[1] != '_')
		error("You are not using the " BMAG "del" NC " function correctly\n");
	free(content);
}

int test_single_lstmap(int test_number, t_list **initial, t_list **expected)
{
	char *list_str = list_to_str(initial);
	set_signature_tn(test_number, "ft_lstmap(%s, [s => __strlen(s)], [x => free(x)])", list_str); free(list_str);

	t_list *res = ft_lstmap(*initial, map_length, delete);
	int result = same_list(expected, &res);
	lstclear(&res, free);
	result = check_leaks(NULL) && result;

#ifdef STRICT_MEM
	reset_malloc_mock();
	ft_lstmap(*initial, map_length, delete);
	int malloc_calls = reset_malloc_mock();
	int no_leaks;
	for (int i = 0; i < malloc_calls; i++)
	{
		sprintf(signature + g_offset, NC " NULL check for %ith malloc", i);
		malloc_set_null(i);
		t_list *res = ft_lstmap(*initial, map_length, delete);
		lstclear(&res, delete);
		no_leaks = check_leaks(NULL);
		if (!no_leaks) {
			fseek(errors_file, -1, SEEK_CUR);
			fprintf(errors_file, "Most likely you are not calling " BMAG "del" NC \
					" on the content when a new list node allocation fails.\n\n");
		}
		result = no_leaks && result;
		if (res != NULL)
			result = error("Should return NULL\n");
	}
#endif
	return result;
}

int test_lstmap()
{
	int res = test_single_lstmap(1, create_list(0), create_list(0));
	res = test_single_lstmap(2, create_list(1, "hello!"), create_list(1, "__6"));
	res = test_single_lstmap(3,
	 	create_list(5, "one", "two", "three", "four", "five"),
	 	create_list(5, "__3", "__3", "__5", "__4", "__4"));
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(lstmap);
}
