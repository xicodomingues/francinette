#include "pf_utils.h"

void simple_test()
{
	TEST("no format", {
		test_printf_noarg("");
		test_printf_noarg("\x01\x02\a\v\b\f\r\n");
	})

	TEST("% format", {
		test_printf_noarg("%%");
		test_printf_noarg(" %%");
		test_printf_noarg("%%c");
		test_printf_noarg("%%%%%%");
		test_printf("%%%c", 'x');
	})
}

void test_c()
{
	TEST("c format", {
		test_printf("%c", 'x');
		test_printf(" %c", 'x');
		test_printf("%c ", 'x');
		test_printf("%c%c%c", 'a', '\t', 'b');
		test_printf("%cc%cc%c", 'a', '\t', 'b');
		test_printf("%cs%cs%c", 'c', 'b', 'a');
	})
}

void test_s()
{
	TEST("s format", {
		test_printf("%s", "");
		test_printf("%s", (char *)NULL);
		test_printf("%s", "some string with %s hehe");
		test_printf(" %s", "can it handle \t and \n?");
		test_printf("%sx", "{} al$#@@@^&$$^#^@@^$*((&");
		test_printf("%s%s%s", "And ", "some", "joined");
		test_printf("%ss%ss%ss", "And ", "some other", "joined");
	})
}

void test_p()
{
	TEST("p format", {
		test_printf("%p", "");
		test_printf("%p", NULL);
		test_printf("%p", (void *)-14523);
		test_printf("0x%p-", (void *)ULONG_MAX);
		test_printf("%pp%p%p", (void *)LONG_MAX + 423856, (void *)0, (void *)INT_MAX);
	})
}

void test_d()
{
	TEST("d format", {
		test_printf("%d", 0);
		test_printf("%d", -10);
		test_printf("%d", -200000);
		test_printf("%d", -6000023);
		test_printf("%d", 10);
		test_printf("%d", 10000);
		test_printf("%d", 100023);
		test_printf("%d", INT_MAX);
		test_printf("%d", INT_MIN);
		test_printf("dgs%dxx", 10);
		test_printf("%d%dd%d", 1, 2, -3);
	})
}

void test_i()
{
	TEST("i format", {
		test_printf("%i", 0);
		test_printf("%i", -10);
		test_printf("%i", -200000);
		test_printf("%i", -6000023);
		test_printf("%i", 10);
		test_printf("%i", 10000);
		test_printf("%i", 100023);
		test_printf("%i", INT_MAX);
		test_printf("%i", INT_MIN);
		test_printf("dgs%ixx", 10);
		test_printf("%i%ii%i", 1, 2, -3);
	})
}

void test_u()
{
	TEST("u format", {
		test_printf("%u", 0);
		test_printf("%u", -10);
		test_printf("%u", -200000);
		test_printf("%u", -6000023);
		test_printf("%u", 10);
		test_printf("%u", 10000);
		test_printf("%u", 100023);
		test_printf("%u", INT_MAX);
		test_printf("%u", INT_MIN);
		test_printf("%u", UINT_MAX);
		test_printf("dgs%uxx", 10);
		test_printf("%u%uu%u", 1, 2, -3);
	})
}

void test_x()
{
	TEST("x format", {
		test_printf("%x", 0);
		test_printf("%x", -10);
		test_printf("%x", -200000);
		test_printf("%x", -6000023);
		test_printf("%x", 10);
		test_printf("%x", 10000);
		test_printf("%x", 100023);
		test_printf("%x", 0xabcdef);
		test_printf("%x", 0x7fedcba1);
		test_printf("%x", INT_MAX);
		test_printf("%x", INT_MIN);
		test_printf("%x", UINT_MAX);
		test_printf("dgs%xxx", 10);
		test_printf("%x%xx%x", 1, 2, -3);
	})
}

void test_X()
{
	TEST("X format", {
		test_printf("%X", 0);
		test_printf("%X", -10);
		test_printf("%X", -200000);
		test_printf("%X", -6000023);
		test_printf("%X", 10);
		test_printf("%X", 10000);
		test_printf("%X", 100023);
		test_printf("%X", 0xabcdef);
		test_printf("%X", 0x7fedcba1);
		test_printf("%X", INT_MAX);
		test_printf("%X", INT_MIN);
		test_printf("%X", UINT_MAX);
		test_printf("dgs%Xxx", 10);
		test_printf("%X%Xx%X", 1, 2, -3);
	})
}

int main(int argn, char **argv)
{
	printf(YEL "Mandatory:" NC "\n");
	pf_setup_framework(argn, argv);

	simple_test();
	test_c();
	test_s();
	test_p();
	test_d();
	test_i();
	test_u();
	test_x();
	test_X();

	TEST("random", {
		// generated in python
		//==%%^^&&++==
	});
}