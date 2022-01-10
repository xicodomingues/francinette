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
	title("ft_memmove\t: ")
	
	char s[] = {65, 66, 67, 68, 69, 0, 45};
	char s0[] = { 0,  0,  0,  0,  0,  0, 0};
	char sCpy[] = {65, 66, 67, 68, 69, 0, 45};
	char sResult[] = {67, 68, 67, 68, 69, 0, 45};
	char sResult2[] = {67, 67, 68, 68, 69, 0, 45};

	/* 1 */ check(ft_memmove(s0, s, 7) == s0 && !memcmp(s, s0, 7)); showLeaks(); //Post 0
	/* 2 */ check(ft_memmove(s, s + 2, 0) && !memcmp(s, sCpy, 7)); showLeaks(); //0 move
	/* 3 */ check(ft_memmove(s, s + 2, 2) == s && !memcmp(s, sResult, 7)); showLeaks(); //forward
	/* 4 */ check(ft_memmove(sResult + 1, sResult, 2) == sResult + 1 && !memcmp(sResult, sResult2, 7)); showLeaks(); //reverse
	write(1, "\n", 1);
	return (0);
}