
#include "utils.h"

create_test_ctype(isprint);

int	main()
{
	set_sigsev();
	test(isprint);
}
