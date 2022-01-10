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

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_lstadd_back\t: ")

	t_list * l =  NULL; t_list * l2 =  NULL; 
	ft_lstadd_back(&l, ft_lstnew((void*)1));
	/* 1 */ check(l->content == (void*)1);
	/* 2 */ check(l->next == 0);

	ft_lstadd_back(&l, ft_lstnew((void*)2));
	/* 3 */ check(l->content == (void*)1);
	/* 4 */ check(l->next->content == (void*)2);
	/* 5 */ check(l->next->next == 0);

	ft_lstadd_back(&l2, ft_lstnew((void*)3));
	ft_lstadd_back(&l2, ft_lstnew((void*)4));
	ft_lstadd_back(&l, l2);
	/* 6 */ check(l->content == (void*)1);
	/* 7 */ check(l->next->content == (void*)2);
	/* 8 */ check(l->next->next->content == (void*)3);
	/* 9 */ check(l->next->next->next->content == (void*)4);
	/* 10 */ check(l->next->next->next->next == 0);
	freeList(l); showLeaks();
	write(1, "\n", 1);
	return (0);
}