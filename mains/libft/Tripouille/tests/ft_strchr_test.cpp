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
	title("ft_strchr\t: ")
	char s[] = "tripouille";
	/* 1 */ check(ft_strchr(s, 't') == s); showLeaks();
	/* 2 */ check(ft_strchr(s, 'l') == s + 7); showLeaks();
	/* 3 */ check(ft_strchr(s, 'z') == 0); showLeaks();
	/* 4 */ check(ft_strchr(s, 0) == s + strlen(s)); showLeaks();
	/* 5 */ check(ft_strchr(s, 't' + 256) == s); showLeaks();
	write(1, "\n", 1);
	return (0);
}