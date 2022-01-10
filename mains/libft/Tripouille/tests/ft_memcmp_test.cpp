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
	title("ft_memcmp\t: ")

	char s[] = {-128, 0, 127, 0};
	char sCpy[] = {-128, 0, 127, 0};
	char s2[] = {0, 0, 127, 0};
	char s3[] = {0, 0, 42, 0};
	/* 1 */ check(!ft_memcmp(s, sCpy, 4)); showLeaks();
	/* 2 */ check(!ft_memcmp(s, s2, 0)); showLeaks();
	/* 3 */ check(ft_memcmp(s, s2, 1) > 0); showLeaks();
	/* 4 */ check(ft_memcmp(s2, s, 1) < 0); showLeaks();
	/* 5 */ check(ft_memcmp(s2, s3, 4) != 0); showLeaks();
	write(1, "\n", 1);
	return (0);
}