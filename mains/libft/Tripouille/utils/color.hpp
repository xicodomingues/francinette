#ifndef COLOR_HPP
# define COLOR_HPP
# include <iostream>
# define ENDL RESET_ALL << std::endl

enum Color
{
	RESET_ALL			= 0,
	RESET_BOLD			= 21,
	RESET_DIM			= 22,
	RESET_UNDERLINED	= 24,
	RESET_BLINK			= 25,
	RESET_REVERSED		= 27,
	RESET_HIDDEN		= 28,

	BOLD				= 1,
	DIM					= 2,
	UNDERLINED			= 4,
	BLINK				= 5,
	REVERSED			= 7,
	HIDDEN				= 8,

	FG_DEFAULT			= 39,
	FG_BLACK			= 30,
	FG_RED				= 31,
	FG_GREEN			= 32,
	FG_YELLOW 			= 33,
	FG_BLUE				= 34,
	FG_MAGENTA			= 35,
	FG_CYAN				= 36,
	FG_LGRAY			= 37,
	FG_DGRAY			= 90,
	FG_LRED				= 91,
	FG_LGREEN			= 92,
	FG_LYELLOW			= 93,
	FG_LBLUE			= 94,
	FG_LMAGENTA			= 95,
	FG_LCYAN			= 96,
	FG_WHITE			= 97,

	BG_DEFAULT			= 49,
	BG_BLACK			= 40,
	BG_RED				= 41,
	BG_GREEN			= 42,
	BG_YELLOW 			= 43,
	BG_BLUE				= 44,
	BG_MAGENTA			= 45,
	BG_CYAN				= 46,
	BG_LGRAY			= 47,
	BG_DGRAY			= 100,
	BG_LRED				= 101,
	BG_LGREEN			= 102,
	BG_LYELLOW			= 103,
	BG_LBLUE			= 104,
	BG_LMAGENTA			= 105,
	BG_LCYAN			= 106,
	BG_WHITE			= 107
};

std::ostream & operator<<(std::ostream & os, Color c);

#endif