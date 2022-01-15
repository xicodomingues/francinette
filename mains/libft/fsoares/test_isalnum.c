
#include "utils.h"

create_test_ctype(isalnum);

int	main()
{
	set_sigsev();
	test(isalnum);
}
