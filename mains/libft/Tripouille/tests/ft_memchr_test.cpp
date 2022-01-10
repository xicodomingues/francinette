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
	title("ft_memchr\t: ")
	
	char s[] = {0, 1, 2 ,3 ,4 ,5};
	/* 1 */ check(ft_memchr(s, 0, 0) == NULL); showLeaks();
	/* 2 */ check(ft_memchr(s, 0, 1) == s); showLeaks();
	/* 3 */ check(ft_memchr(s, 2, 3) == s + 2); showLeaks();
	/* 4 */ check(ft_memchr(s, 6, 6) == NULL); showLeaks();
	/* 5 */ check(ft_memchr(s, 2 + 256, 3) == s + 2); showLeaks(); //Cast check
	write(1, "\n", 1);
	return (0);
}