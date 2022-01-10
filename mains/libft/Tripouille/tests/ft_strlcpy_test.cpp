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
	title("ft_strlcpy\t: ")
	
	char src[] = "coucou";
	char dest[10]; memset(dest, 'A', 10);
	/* 1 */ check(ft_strlcpy(dest, src, 0) == strlen(src) && dest[0] == 'A'); showLeaks();
	/* 2 */ check(ft_strlcpy(dest, src, 1) == strlen(src) && dest[0] == 0 && dest[1] == 'A'); showLeaks();
	/* 3 */ check(ft_strlcpy(dest, src, 2) == strlen(src) && dest[0] == 'c' && dest[1] == 0  && dest[2] == 'A'); showLeaks();
	/* 4 */ check(ft_strlcpy(dest, src, -1) == strlen(src) && !strcmp(src, dest) && dest[strlen(src) + 1] == 'A'); showLeaks(); memset(dest, 'A', 10);
	/* 5 */ check(ft_strlcpy(dest, src, 6) == strlen(src) && !memcmp(src, dest, 5) && dest[5] == 0); showLeaks(); memset(dest, 'A', 10);
	/* 6 */ check(ft_strlcpy(dest, src, 7) == strlen(src) && !memcmp(src, dest, 7)); showLeaks(); memset(dest, 'A', 10);
	/* 7 */ check(ft_strlcpy(dest, src, 8) == strlen(src) && !memcmp(src, dest, 7)); showLeaks(); memset(dest, 'A', 10);
	/* 8 */ check(ft_strlcpy(dest, "", 42) == 0 && !memcmp("", dest, 1)); showLeaks(); memset(dest, 0, 10);
	/* 9 */ check(ft_strlcpy(dest, "1", 0) == 1 && dest[0] == 0); showLeaks(); memset(dest, 'A', 10);
	write(1, "\n", 1);
	return (0);
}