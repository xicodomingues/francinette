
#include "my_utils.h"

int single_test_putchar(int test_n, char c, int fd)
{
	set_signature_tn(test_n, "ft_putchar_fd(%i:%s, fd: %i)", c, escape_chr(c), fd);

	ft_putchar_fd(c, fd);
	return check_leaks(NULL);
}

int test_putchar_fd()
{
	int fd = open("fsoares", O_RDWR | O_CREAT);

	int res = single_test_putchar(1, 'a', fd);
	res = single_test_putchar(2, 'x', fd) && res;
	res = single_test_putchar(3, 'y', fd) && res;
	res = single_test_putchar(4, 'z', fd) && res;
	res = single_test_putchar(5, '\n', fd) && res;

	lseek(fd, SEEK_SET, 0);
	char content[10] = {0};
	read(fd, content, 10);

	char *expected = "axyz\n";
	if(strcmp(content, expected) != 0)
		res = error("expected: %s, content of the file: %s\n", escape_str(expected), escape_str(content)) && res;

	set_signature_tn(6, "ft_putchar_fd(%i:%s, fd: %i)", 't', escape_chr('t'), fd);
	null_null_check(ft_putchar_fd('t', fd), res);

	remove("./fsoares");
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(putchar_fd);
}
