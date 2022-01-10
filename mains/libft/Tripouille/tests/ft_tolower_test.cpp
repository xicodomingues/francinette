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
	title("ft_tolower\t: ")
	
	/* 1 */ check(ft_tolower('A' - 1) == 'A' - 1); showLeaks();
	/* 2 */ check(ft_tolower('A') == 'a'); showLeaks();
	/* 3 */ check(ft_tolower('Z' + 1) == 'Z' + 1); showLeaks();
	/* 4 */ check(ft_tolower('Z') == 'z'); showLeaks();
	write(1, "\n", 1);
	return (0);
}