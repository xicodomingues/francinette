#include "check.hpp"
#include "leaks.hpp"

extern int iTest;

void check(bool succes)
{
	if (succes)
		{std::ostringstream ss; ss << FG_GREEN << iTest++ << ".OK "; write(1, ss.str().c_str(), ss.str().size());}
	else
		{std::ostringstream ss; ss << FG_RED << iTest++ << ".KO "; write(1, ss.str().c_str(), ss.str().size());}
}

void mcheck(void * p, size_t required_size)
{
	void * p2 = malloc(required_size); 
	#ifdef __unix__
	if (malloc_usable_size(p) == malloc_usable_size(p2))
	#endif
	#ifdef __APPLE__
	if (malloc_size(p) == malloc_size(p2))
	#endif
		{std::ostringstream ss; ss << FG_GREEN << iTest++ << ".MOK "; write(1, ss.str().c_str(), ss.str().size());}
	else
		{std::ostringstream ss; ss << FG_RED << iTest++ << ".MKO "; write(1, ss.str().c_str(), ss.str().size());}
	free(p2);
}
