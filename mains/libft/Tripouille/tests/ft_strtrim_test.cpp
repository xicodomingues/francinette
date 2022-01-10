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
	title("ft_strtrim\t: ")

	char * s = ft_strtrim("   xxxtripouille", " x");
	/* 1 */ check(!strcmp(s, "tripouille"));
	/* 2 */ mcheck(s, strlen("tripouille") + 1); free(s); showLeaks();

	s = ft_strtrim("tripouille   xxx", " x");
	/* 3 */ check(!strcmp(s, "tripouille"));
	/* 4 */ mcheck(s, strlen("tripouille") + 1); free(s); showLeaks();

	s = ft_strtrim("   xxxtripouille   xxx", " x");
	/* 5 */ check(!strcmp(s, "tripouille"));
	/* 6 */ mcheck(s, strlen("tripouille") + 1); free(s); showLeaks();
	
	s = ft_strtrim("   xxx   xxx", " x");
	/* 7 */ check(!strcmp(s, ""));
	/* 8 */ mcheck(s, 1); free(s); showLeaks();

	s = ft_strtrim("", "123");
	/* 9 */ check(!strcmp(s, ""));
	/* 10 */ mcheck(s, 1); free(s); showLeaks();

	s = ft_strtrim("123", "");
	/* 11 */ check(!strcmp(s, "123"));
	/* 12 */ mcheck(s, 4); free(s); showLeaks();

	s = ft_strtrim("", "");
	/* 13 */ check(!strcmp(s, ""));
	/* 14 */ mcheck(s, 1); free(s); showLeaks();
	
	s = ft_strtrim("abcdba", "acb");
	/* opsec-infosec 15 */ check(!strcmp(s, "d"));
 	/* opsec-infosec 16 */ mcheck(s, 2); free(s); showLeaks();
	
	write(1, "\n", 1);
	return (0);
}
