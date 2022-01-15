
#include "utils.h"

create_test_ctype(isascii);

int	main()
{
	set_sigsev();
	test(isascii);
}
