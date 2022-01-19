
#include "utils.h"

int test_single_substr(char *str, unsigned int start, size_t size, char *expected)
{
	set_sign("substr(\"%s\", %u, %zu)", str, start, size);

	char *res = ft_substr(str, start, size);

	int result = same_string(expected, res);
	result = check_leaks(res) && result;

	null_check(ft_substr(str, start, size), result);
	return result;
}

int test_substr()
{
	int res = 1;
	res = test_single_substr("", 0, 0, "") && res;
	res = test_single_substr("", 0, 1, "") && res;
	res = test_single_substr("", 1, 1, "") && res;
	res = test_single_substr("hola", -1, 0, "") && res;
	res = test_single_substr("hola", 0, -1, "hola") && res;
	res = test_single_substr("hola", -1, -1, "") && res;
	res = test_single_substr("hola", 0, 0, "") && res;
	res = test_single_substr("hola", 0, 1, "h") && res;
	res = test_single_substr("hola", 0, 3, "hol") && res;
	res = test_single_substr("hola", 0, 4, "hola") && res;
	res = test_single_substr("hola", 0, 5, "hola") && res;
	res = test_single_substr("hola", 2, 0, "") && res;
	res = test_single_substr("hola", 2, 1, "l") && res;
	res = test_single_substr("hola", 2, 2, "la") && res;
	res = test_single_substr("hola", 2, 3, "la") && res;
	res = test_single_substr("hola", 2, 30, "la") && res;
	res = test_single_substr("hola", 3, 0, "") && res;
	res = test_single_substr("hola", 3, 1, "a") && res;
	res = test_single_substr("hola", 3, 2, "a") && res;
	res = test_single_substr("hola", 4, 0, "") && res;
	res = test_single_substr("hola", 4, 1, "") && res;
	res = test_single_substr("hola", 4, 20, "") && res;
	res = test_single_substr("hola", 5, 2, "") && res;

	return res;
}

int main()
{
	handle_signals();
	test(substr);
}
