extern "C"
{
#define new tripouille
#include "libft.h"
#undef new
}

#include "sigsegv.hpp"
#include "check.hpp"
#include "leaks.hpp"
#include <string.h>

void freeList(t_list *head) {if (head) freeList(head->next); free(head);}
void * addOne(void * p) {void * r = malloc(sizeof(int)); *(int*)r = *(int*)p + 1; return (r);}

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_lstmap\t: ")

	int tab[] = {0, 1, 2, 3};
	t_list * l =  ft_lstnew(tab);
	for (int i = 1; i < 4; ++i)
		ft_lstadd_back(&l, ft_lstnew(tab + i));
	t_list * m = ft_lstmap(l, addOne, free);
	t_list * tmp = l;
	/* 1 2 3 4 */ for (int i = 0; i < 4; ++i)
	{
		check(*(int*)tmp->content == i);
		tmp = tmp->next;
	}
	tmp = m;
	/* 5 6 7 8 */ for (int i = 0; i < 4; ++i)
	{
		check(*(int*)tmp->content == i + 1);
		tmp = tmp->next;
	}
	freeList(l); ft_lstclear(&m, free); showLeaks();
	write(1, "\n", 1);
	return (0);
}