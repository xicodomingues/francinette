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
#include <climits>

int iTest = 1;
int main(void)
{
	signal(SIGSEGV, sigsegv);
	title("ft_putnbr_fd\t: ")

	int fd = open("tripouille", O_RDWR | O_CREAT, 0777);
	ft_putnbr_fd(0, fd);
	lseek(fd, SEEK_SET, 0);
	char s[42] = {0}; read(fd, s, 2);
	/* 1 */ check(!strcmp(s, "0")); showLeaks();
	unlink("./tripouille");

	fd = open("tripouille", O_RDWR | O_CREAT, 0777);
	ft_putnbr_fd(10, fd);
	lseek(fd, SEEK_SET, 0);
	read(fd, s, 3);
	/* 2 */ check(!strcmp(s, "10")); showLeaks();
	unlink("./tripouille");

	fd = open("tripouille", O_RDWR | O_CREAT, 0777);
	ft_putnbr_fd(INT_MAX, fd);
	lseek(fd, SEEK_SET, 0);
	read(fd, s, 11);
	/* 3 */ check(!strcmp(s, to_string(INT_MAX).c_str())); showLeaks();
	unlink("./tripouille");

	fd = open("tripouille", O_RDWR | O_CREAT, 0777);
	ft_putnbr_fd(INT_MIN, fd);
	lseek(fd, SEEK_SET, 0);
	read(fd, s, 12);
	/* 4 */ check(!strcmp(s, to_string(INT_MIN).c_str())); showLeaks();
	unlink("./tripouille");

	fd = open("tripouille", O_RDWR | O_CREAT, 0777);
	ft_putnbr_fd(-42, fd);
	lseek(fd, SEEK_SET, 0);
	s[read(fd, s, 4)] = 0;
	/* 5 ipenas */ check(!strcmp(s, "-42")); showLeaks();
	unlink("./tripouille");
	write(1, "\n", 1);
	return (0);
}
