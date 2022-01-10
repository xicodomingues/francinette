#ifndef LEAK_HPP
# define LEAK_HPP
# include <stdlib.h>
# include <vector>
# include <iostream>
# include <sstream>
# include <unistd.h>
# include <stdlib.h>
# include <dlfcn.h>
# include <algorithm>
# include "color.hpp"


using std::endl;
struct ptr
{
	void * p;
	size_t size;
	ptr(void * _p = 0, size_t _size = 0) : p(_p), size(_size) {}
};

bool operator==(ptr const & p1, ptr const & p2);

extern std::vector<ptr> mallocList;

void mallocListAdd(void * p, size_t size);
void mallocListRemove(void * p);
void showLeaks(void);

#endif