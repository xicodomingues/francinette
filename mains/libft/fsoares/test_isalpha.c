#include "utils.h"

create_test_ctype(isalpha);

int	main()
{
	set_sigsev();
	test(isalpha);
}
