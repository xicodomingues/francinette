
#include "my_utils.h"

int single_test_putendl(int test_number, char *str, int fd)
{
	set_signature_tn(test_number, "ft_putendl_fd(%s, fd: %i)", escape_str(str), fd);

	ft_putendl_fd(str, fd);
	return check_leaks(NULL);
}

int test_putendl_fd()
{
	int fd = open("fsoares", O_RDWR | O_CREAT);

	int res = single_test_putendl(1, "", fd);
	res = single_test_putendl(2, "abcdef", fd) && res;
	res = single_test_putendl(3, "1234", fd) && res;
	res = single_test_putendl(4, "567", fd) && res;
	res = single_test_putendl(5, "end!", fd) && res;

	lseek(fd, SEEK_SET, 0);
	char content[100] = {0};
	read(fd, content, 100);

	char *expected = "\nabcdef\n1234\n567\nend!\n";
	if(strcmp(content, expected) != 0)
		res = error("expected: %s, content of the file: %s\n", escape_str(expected), escape_str(content)) && res;

	set_signature_tn(6, "ft_putendl_fd(\"%s\", fd: %i)", "teste", fd);
	null_null_check(ft_putendl_fd("teste", fd), res);

	remove("./fsoares");
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(putendl_fd);
}
