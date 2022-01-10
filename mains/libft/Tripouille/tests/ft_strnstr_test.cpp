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
	title("ft_strnstr\t: ")

	char haystack[30] = "aaabcabcd";
	char needle[10] = "aabc";
	char * empty = (char*)"";
	/* 1 */ check(ft_strnstr(haystack, needle, 0) == 0); showLeaks();
	/* 2 */ check(ft_strnstr(haystack, needle, -1) == haystack + 1); showLeaks();
	/* 3 */ check(ft_strnstr(haystack, "a", -1) == haystack); showLeaks();
	/* 4 */ check(ft_strnstr(haystack, "c", -1) == haystack + 4); showLeaks();
	/* 5 */ check(ft_strnstr(empty, "", -1) == empty); showLeaks();
	/* 6 */ check(ft_strnstr(empty, "", 0) == empty); showLeaks();
	/* 7 */ check(ft_strnstr(empty, "coucou", -1) == 0); showLeaks();
	/* 8 */ check(ft_strnstr(haystack, "aaabc", 5) == haystack); showLeaks();
	/* 9 */ check(ft_strnstr(empty, "12345", 5) == 0); showLeaks();
	/* 10 */ check(ft_strnstr(haystack, "abcd", 9) == haystack + 5); showLeaks();
	/* 11 */ check(ft_strnstr(haystack, "cd", 8) == NULL); showLeaks();
	/* 12 mbueno-g */ check(ft_strnstr(haystack, "a", 1) == haystack); showLeaks();
	/* 13 opsec-infosec */ check(ft_strnstr("1", "a", 1) == NULL); showLeaks();
	/* 14 opsec-infosec */ check(ft_strnstr("22", "b", 2) == NULL); showLeaks();
	write(1, "\n", 1);
	return (0);
}
