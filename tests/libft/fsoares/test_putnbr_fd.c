/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_putnbr_fd.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kjullien <kjullien@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/11/19 21:09:16 by kjullien          #+#    #+#             */
/*   Updated: 2024/11/19 21:40:27 by kjullien         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "my_utils.h"

int single_test_putnbr(int test_number, int n, int fd)
{
	set_signature_tn(test_number, "ft_putnbr_fd(%i, fd: %i)", n, fd);

	ft_putnbr_fd(n, fd);
	ft_putendl_fd("", fd);
	return check_leaks(NULL);
}

int test_putnbr_fd()
{
	int fd = open("fsoares", O_RDWR | O_CREAT, S_IRWXU);

	int res = single_test_putnbr(1, 0, fd);
	res = single_test_putnbr(2, 10000043, fd) && res;
	res = single_test_putnbr(3, -10000043, fd) && res;
	res = single_test_putnbr(4, INT_MAX, fd) && res;
	res = single_test_putnbr(5, INT_MIN, fd) && res;

	lseek(fd, SEEK_SET, 0);
	char content[100] = {0};
	int res2 = read(fd, content, 100);
	(void)res2;

	char expected[1000];
	sprintf(expected, "0\n10000043\n-10000043\n%i\n%i\n", INT_MAX, INT_MIN);
	if(strcmp(content, expected) != 0)
		res = error("expected: %s, content of the file: %s\n", escape_str(expected), escape_str(content)) && res;

	set_signature_tn(6, "ft_putnbr_fd(%i, fd: %i)", 10000, fd);
	null_null_check(ft_putnbr_fd(10000, fd), res);

	close(fd);
	remove("./fsoares");
	return res;
}

int	main()
{
	handle_signals_with_time();
	test(putnbr_fd);
}
