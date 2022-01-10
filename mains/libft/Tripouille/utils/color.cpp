#include "color.hpp"

std::ostream &
operator<<(std::ostream & os, Color c)
{
	return os << "\e[" << static_cast<int>(c) << "m";
}