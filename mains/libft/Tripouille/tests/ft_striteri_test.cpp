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

void
iter(unsigned int i, char * s) {
	*s += i;
}

int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_striteri\t: ")

	{
		char s[] = "";
		ft_striteri(s, iter);
		/* 1 */ check(!strcmp(s, ""));
	}

	{
		char s[] = "0";
		ft_striteri(s, iter);
		/* 2 */ check(!strcmp(s, "0"));
	}

	{
		char s[] = "0000000000";
		ft_striteri(s, iter);
		/* 3 */ check(!strcmp(s, "0123456789"));
	}
	write(1, "\n", 1);
	return (0);
}