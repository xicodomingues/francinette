
#include "utils.h"

create_test_ctype(isdigit);

int	main()
{
	set_sigsev();
	test(isdigit);
}
