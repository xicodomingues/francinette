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
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_putstr_fd\t: ")

	int fd = open("tripouille", O_RDWR | O_CREAT);
	ft_putstr_fd((char*)"42", fd);
	lseek(fd, SEEK_SET, 0);
	char s[10] = {0}; read(fd, s, 3);
	/* 1 */ check(!strcmp(s, "42")); showLeaks();
	unlink("./tripouille");
	write(1, "\n", 1);
	return (0);
}