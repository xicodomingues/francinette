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
	title("ft_lstadd_front\t: ")

	t_list * l =  NULL;
	ft_lstadd_front(&l, ft_lstnew((void*)1));
	/* 1 */ check(l->content == (void*)1);
	/* 2 */ check(l->next == 0);

	ft_lstadd_front(&l, ft_lstnew((void*)2));
	/* 3 */ check(l->content == (void*)2);
	/* 4 */ check(l->next->content == (void*)1);
	/* 5 */ check(l->next->next == 0); 
	freeList(l); showLeaks();
	write(1, "\n", 1);
	return (0);
}