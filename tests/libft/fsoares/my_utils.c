#include "my_utils.h"

void handle_signals_with_time()
{
	alarm(TIMEOUT);
	handle_signals();
}

int set_signature_tn(int test_number, const char *format, ...)
{
	g_test = test_number;
	va_list args;
	va_start(args, format);
	g_offset = vsprintf(signature, format, args);
	va_end(args);
	reset_malloc_mock();
	return g_offset;
}
