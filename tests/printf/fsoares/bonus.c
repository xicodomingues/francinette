#include "pf_utils.h"

// generated in python
//==%%^^&&++==

int main(int argn, char **argv)
{
	printf(YEL "\nBonus:" NC "\n");
	pf_setup_framework(argn, argv);

	test_c();
	test_s();
	test_p();
	test_d();
	test_i();
	test_u();
	test_x();
	test_X();
	test_percent();
}