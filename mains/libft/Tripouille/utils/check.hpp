#ifndef CHECK_HPP
# define CHECK_HPP
# include <iostream>
# include <string>
# include <sstream>
# include <unistd.h>
# include "color.hpp"

# ifdef __unix__
#  include <malloc.h>
# endif
# ifdef __APPLE__
#  include <stdlib.h>
#  include <malloc/malloc.h>
# endif

#define title(s) {std::ostringstream ss; ss << FG_LGRAY << s; write(1, ss.str().c_str(), ss.str().size());}
using namespace std;

void check(bool succes);
void mcheck(void * p, size_t required_size);

#endif