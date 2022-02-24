#include "pf_utils.h"

int main(int argn, char **argv)
{
	pf_setup_framework(argn, argv);

	TEST("%c format", {
		test_printf("%c", 'x');
		test_printf(" %c", 'x');
		test_printf("%c ", 'x');
		test_printf("%c%c%c", 'a', '\t', 'b');
		test_printf("%cc%cc%c", 'a', '\t', 'b');
		test_printf("%cs%cs%c", 'c', 'b', 'a');
	})

	TEST("%s format", {
		test_printf("%s", "");
		test_printf("%s", "some string with %s hehe");
		test_printf(" %s", "can it handle \t and \n?");
		test_printf("%s%s%s", "And ", "some", "joined");
		test_printf("%ss%ss%ss", "And ", "some other", "joined");
	})

	TEST("%% format", {
		test_printf_noarg("%%");
		test_printf_noarg(" %%");
		test_printf_noarg("%%c");
		test_printf_noarg("%%%%%%");
	})
}