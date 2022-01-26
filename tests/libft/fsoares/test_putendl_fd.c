
#include "utils.h"

int single_test_putendl(char *str, int fd)
{
	set_sign("ft_putendl_fd(%s, fd: %i)", escape_str(str), fd);

	ft_putendl_fd(str, fd);
	return check_leaks(NULL);
}

int test_putendl_fd()
{
	int fd = open("fsoares", O_RDWR | O_CREAT);

	int res = single_test_putendl("", fd);
	res = single_test_putendl("abcdef", fd) && res;
	res = single_test_putendl("1234", fd) && res;
	res = single_test_putendl("\b567", fd) && res;
	res = single_test_putendl("end!", fd) && res;

	lseek(fd, SEEK_SET, 0);
	char content[100] = {0};
	read(fd, content, 100);

	char *expected = "\nabcdef\n1234\n\b567\nend!\n";
	if(strcmp(content, expected) != 0)
		res = error("expected: %s, content of the file: %s\n", escape_str(expected), escape_str(content)) && res;

	set_sign("ft_putendl_fd(\"%s\", fd: %i)", "teste", fd);
	null_null_check(ft_putendl_fd("teste", fd), res);

	remove("./fsoares");
	return res;
}

int	main()
{
	handle_signals();
	test(putendl_fd);
}
