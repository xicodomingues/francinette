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
#include <climits>

char addOne(unsigned int i, char c) {return (i + c);}

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_strmapi\t: ")

	char * s = ft_strmapi("1234", addOne);
	/* 1 */ check(!strcmp(s, "1357"));
	/* 2 */ mcheck(s, strlen("1357") + 1); free(s); showLeaks();

	s = ft_strmapi("", addOne);
	/* 3 */ check(!strcmp(s, ""));
	/* 4 */ mcheck(s, strlen("") + 1); free(s); showLeaks();
	write(1, "\n", 1);
	return (0);
}