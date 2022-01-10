#include "sigsegv.hpp"
#include "color.hpp"

extern int iTest;

void sigsegv(int signal)
{
	(void)signal;
	cout << FG_LYELLOW << iTest++ << ".SIGSEGV" << ENDL;
	exit(EXIT_SUCCESS);
}
