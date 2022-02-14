
#include "my_utils.h"

int single_test_putstr(int test_number, char *str, int fd)
{
	set_signature_tn(test_number, "ft_putstr_fd(%s, fd: %i)", escape_str(str), fd);

	ft_putstr_fd(str, fd);
	return check_leaks(NULL);
}

int test_putstr_fd()
{
	int fd = open("fsoares", O_RDWR | O_CREAT);

	int res = single_test_putstr(1, "abcdef", fd);
	res = single_test_putstr(2, "\n1234", fd) && res;
	res = single_test_putstr(3, "\t567", fd) && res;
	res = single_test_putstr(4, "", fd) && res;
	res = single_test_putstr(5, "\nend!", fd) && res;

	lseek(fd, SEEK_SET, 0);
	char content[100] = {0};
	read(fd, content, 100);

	char *expected = "abcdef\n1234\t567\nend!";
	if(strcmp(content, expected) != 0)
		res = error("expected: %s, content of the file: %s\n", escape_str(expected), escape_str(content)) && res;

	set_signature_tn(6, "ft_putstr_fd(\"%s\", fd: %i)", "teste", fd);
	null_null_check(ft_putstr_fd("teste", fd), res);

	remove("./fsoares");
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(putstr_fd);
}
