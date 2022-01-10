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

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_bzero\t: ")
	
	char tab[100];
	memset(tab, 'A', 100);
	ft_bzero(tab, 0);
	/* 1 */ check(tab[0] == 'A'); showLeaks();
	ft_bzero(tab, 42);
	int i = 0;
	for (; i < 100 && tab[i] == 0; ++i)
		;
	/* 2 */ check(i == 42 && tab[42] == 'A'); showLeaks();
	memset(tab, 'A', 100); tab[0] = 0;
	ft_bzero(tab, 42);
	i = 0;
	for (; i < 100 && tab[i] == 0; ++i)
		;
	/* 3 */ check(i == 42); showLeaks();
	write(1, "\n", 1);
	return (0);
}