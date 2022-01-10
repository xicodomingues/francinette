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
	title("ft_isprint\t: ")

	/* 1 */ check(!ft_isprint(' ' - 1)); showLeaks();
	/* 2 */ check(ft_isprint(' ')); showLeaks();
	/* 3 */ check(!ft_isprint('~' + 1)); showLeaks();
	/* 4 */ check(ft_isprint('~')); showLeaks();
	write(1, "\n", 1);
	return (0);
}