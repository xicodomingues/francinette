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
	title("ft_strncmp\t: ")
	
	/* 1 */ check(ft_strncmp("t", "", 0) == 0); showLeaks();
	/* 2 */ check(ft_strncmp("1234", "1235", 3) == 0); showLeaks();
	/* 3 */ check(ft_strncmp("1234", "1235", 4) < 0); showLeaks();
	/* 4 */ check(ft_strncmp("1234", "1235", -1) < 0); showLeaks();
	/* 5 */ check(ft_strncmp("", "", 42) == 0); showLeaks();
	/* 6 */ check(ft_strncmp("Tripouille", "Tripouille", 42) == 0); showLeaks();
	/* 7 */ check(ft_strncmp("Tripouille", "tripouille", 42) < 0); showLeaks();
	/* 8 */ check(ft_strncmp("Tripouille", "TriPouille", 42) > 0); showLeaks();
	/* 9 */ check(ft_strncmp("Tripouille", "TripouillE", 42) > 0); showLeaks();
	/* 10 */ check(ft_strncmp("Tripouille", "TripouilleX", 42) < 0); showLeaks();
	/* 11 */ check(ft_strncmp("Tripouille", "Tripouill", 42) > 0); showLeaks();
	/* 12 */ check(ft_strncmp("", "1", 0) == 0); showLeaks();
	/* 13 */ check(ft_strncmp("1", "", 0) == 0); showLeaks();
	/* 14 */ check(ft_strncmp("", "1", 1) < 0); showLeaks();
	/* 15 */ check(ft_strncmp("1", "", 1) > 0); showLeaks();
	/* 16 */ check(ft_strncmp("", "", 1) == 0); showLeaks();
	write(1, "\n", 1);
	return (0);
}