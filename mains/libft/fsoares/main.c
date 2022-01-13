#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <signal.h>
#include <stdarg.h>

#include "libft.h"
#include "tests.h"
#include "color.h"

#define create_test_ctype(fn)                              \
	int test_##fn(void)                                    \
	{                                                      \
		int c;                                             \
		int res = 1;                                       \
		for (c = 0; c <= 0xff; c++)                        \
		{                                                  \
			if (!fn(c) != !ft_##fn(c))                     \
			{                                              \
				printf(#fn "(%i) std: %i, yours: %i\n", c, \
					   fn(c), ft_##fn(c));                 \
				res = 0;                                   \
			}                                              \
		}                                                  \
		if (!fn(EOF) != !ft_##fn(EOF))                     \
		{                                                  \
			printf(#fn "(EOF) std: %i, yours: %i\n",       \
				   fn(EOF), ft_##fn(EOF));                 \
			res = 0;                                       \
		}                                                  \
		return res;                                        \
	}

#define create_test_val(fn)                                \
	int test_##fn(void)                                    \
	{                                                      \
		int c;                                             \
		int res = 1;                                       \
		for (c = 0; c <= 0xff; c++)                        \
		{                                                  \
			if (fn(c) != ft_##fn(c))                       \
			{                                              \
				printf(#fn "(%i) std: %i, yours: %i\n", c, \
					   fn(c), ft_##fn(c));                 \
				res = 0;                                   \
			}                                              \
		}                                                  \
		if (fn(EOF) != ft_##fn(EOF))                       \
		{                                                  \
			printf(#fn "(EOF) std: %i, yours: %i\n",       \
				   fn(EOF), ft_##fn(EOF));                 \
			res = 0;                                       \
		}                                                  \
		return res;                                        \
	}

#define test(fn)                                   \
	strcpy(function, #fn);                         \
	if (!test_##fn())                              \
		printf("%-10s: " RED "KO" NC "\n\n", #fn); \
	else                                           \
		printf("%-10s: " GRN "OK" NC "\n", #fn);

void print_mem(void *ptr, int size);
void print_mem_full(void *ptr, int size);

char function[1000];
char escaped[1000];

char *rand_bytes(char *dest, int len)
{
	dest[len - 1] = '\0';
	for (int i = 0; i < len - 1; i++)
	{
		dest[i] = rand() % 0x100;
	}
	return dest;
}

create_test_ctype(isalpha);
create_test_ctype(isdigit);
create_test_ctype(isalnum);
create_test_ctype(isascii);
create_test_ctype(isprint);
create_test_val(toupper);
create_test_val(tolower);

#define REPETITIONS 1000

int where_buffer = 0;
char *escape_str(char *src)
{
	int i, j;
	where_buffer = (where_buffer + 1) % 5;
	char *my_bf = escaped + where_buffer * 200;
	for (i = 0, j = 0; src[i]; i++, j++)
	{
		if (isprint(src[i]))
		{
			my_bf[j] = src[i];
		}
		else
		{
			sprintf(my_bf + j, "\\x%02x", (unsigned char)src[i]);
			j += 2;
		}
	}
	my_bf[j] = '\0';
	return my_bf;
}

char *escape_chr(char ch)
{
	if (ch == '\0')
	{
		strcpy(escaped, "'\\x0'");
		return escaped;
	}
	else
	{
		char to_escape[20] = "' '";
		to_escape[1] = ch;
		return escape_str(to_escape);
	}
}

void reset(void *m1, void *m2, int size)
{
	memset(m1, 0x11, size);
	memset(m2, 0x11, size);
}

void reset_with(void *m1, void *m2, char *content, int size)
{
	memset(m1, 0x11, size);
	memset(m2, 0x11, size);
	strcpy(m1, content);
	strcpy(m2, content);
}

void error(const char *format, ...)
{
	printf(RED "Error" NC ": " CYN "%s" NC ": ", function);
	va_list args;
	va_start(args, format);
	vprintf(format, args);
	va_end(args);
}

int same_ptr(void *res, void *res_std)
{
	if (res != res_std)
	{
		error("yours: %p, std: %p\n", res, res_std);
		return 0;
	}
	return 1;
}

int same_mem(void *s, void *r, int size)
{
	int equal = 1;
	char *std = s;
	char *res = r;
	for (int i = 0; i < size; i++)
	{
		if (std[i] != res[i])
		{
			equal = 0;
		}
	}
	if (!equal)
	{
		error("different memory" NC "\n");
		printf(YEL "res" NC ":\n");
		print_mem(res, size);
		printf(YEL "std" NC ":\n");
		print_mem(std, size);
	}
	return equal;
}

int same_value(int res, int res_std)
{
	if (res != res_std)
	{
		error("yours: %i, std: %i\n", res, res_std);
		return 0;
	}
	return 1;
}

int same_sign(int res, int res_std)
{
	int rs = (res > 0 ? 1 : (res < 0 ? -1 : 0));
	int rss = (res_std > 0 ? 1 : (res_std < 0 ? -1 : 0));
	if (rs != rss)
	{
		error("yours: %i (%i), std: %i (%i)\n", rs, res, rss, res_std);
		return 0;
	}
	return 1;
}

#define MEM_SIZE 0x100

#ifdef TEST_STRLEN
int compare_strlen(char *str)
{
	sprintf(function, "ft_strlen(\"%s\")", escape_str(str));
	return same_value(ft_strlen(str), strlen(str));
}

int test_strlen(void)
{
	char str[100];
	int res = 1;

	for (int n = 0; n < REPETITIONS && res; n++)
	{
		rand_bytes(str, rand() % 98 + 1);
		res = compare_strlen(str) && res;
	}
	res = compare_strlen("") && res;
	str[0] = EOF;
	str[1] = '\0';
	res = compare_strlen(str) && res;
	return res;
}
#endif

#ifdef TEST_MEMSET
int single_test_memset(char *m, char *ms, int c, int size)
{
	char *res;
	char *res_std;

	reset(m, ms, MEM_SIZE);
	res_std = memset(ms, c, size);
	res = ft_memset(m, c, size);
	sprintf(function, "ft_memset(mem, %i, %i)", c, size);
	return (same_ptr(res, m) && same_mem(res_std, res, MEM_SIZE));
}

int test_memset(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_memset(mem, mem_std, 'x', 0) && res;
	res = single_test_memset(mem, mem_std, 'g', 12) && res;
	res = single_test_memset(mem, mem_std, 300, 12) && res;
	res = single_test_memset(mem, mem_std, 257, 19) && res;

	int m2[MEM_SIZE];
	int ms2[MEM_SIZE];

	reset(m2, ms2, MEM_SIZE);
	int *rs = memset(ms2 + 1, 143562, 4);
	int *r = ft_memset(m2 + 1, 143562, 4);

	sprintf(function, "ft_memset(ptr, %i, %i)", 143562, 4);
	res = (same_ptr(r, m2 + 1) && same_mem(rs - 1, r - 1, 0x10)) && res;
	return res;
}
#endif

#ifdef TEST_BZERO
int single_test_bzero(char *m, char *ms, int size)
{
	reset(m, ms, MEM_SIZE);
	bzero(ms, size);
	ft_bzero(m, size);
	sprintf(function, "ft_bzero(ptr, %i)", size);
	return (same_mem(ms, m, MEM_SIZE));
}

int test_bzero(void)
{
	char mem[MEM_SIZE];
	char mem_std[MEM_SIZE];

	int res = 1;

	res = single_test_bzero(mem, mem_std, 0) && res;
	res = single_test_bzero(mem, mem_std, 12) && res;
	res = single_test_bzero(mem + 2, mem_std + 2, 40) && res;

	return res;
}
#endif

#ifdef TEST_MEMCPY
int single_test_memcpy(char *dest, char *dest_std, char *src, char *src_std)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);

	rand_bytes(src + 6, rand() % 55 + 1);
	memcpy(src_std + 6, src + 6, 100);

	char *res = ft_memcpy(dest, src, 100);
	char *res_std = memcpy(dest_std, src_std, 100);

	sprintf(function, "ft_memcpy(dest, src, %i)", 100);
	return (same_ptr(res, dest) && same_mem(res_std, res, MEM_SIZE));
}

int test_memcpy(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	char src[MEM_SIZE];
	char src_std[MEM_SIZE];

	int res = 1;
	for (int n = 0; n < REPETITIONS && res; n++)
		res = single_test_memcpy(dest, dest_std, src, src_std) && res;

	return res;
}
#endif

#ifdef TEST_MEMMOVE
int single_test_memmove(char *dest, char *dest_std, char *src, char *src_std)
{
	reset(dest, dest_std, MEM_SIZE);
	reset(src, src_std, MEM_SIZE);

	rand_bytes(src + 6, rand() % 55 + 1);
	memmove(src_std + 6, src + 6, 100);

	char *r = ft_memmove(dest, src, 100);
	char *rs = memmove(dest_std, src_std, 100);
	sprintf(function, "ft_memmove(dest, src, %i)", 100);
	return (same_ptr(r, dest) && same_mem(rs, r, MEM_SIZE));
}

int test_memmove(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	char src[MEM_SIZE];
	char src_std[MEM_SIZE];

	int res = 1;
	for (int n = 0; n < REPETITIONS; n++)
		res = single_test_memmove(dest, dest_std, src, src_std) && res;

	return res;
}
#endif

#ifdef TEST_STRLCPY
int single_test_strlcpy(char *dest, char *dest_std, char *src, int n)
{
	int result = 1;
	reset(dest, dest_std, MEM_SIZE);

	sprintf(function, "ft_strlcpy(dest, \"%s\", %i)", src, n);

	int res = ft_strlcpy(dest, src, n);
	int res_std = strlcpy(dest_std, src, n);
	result = same_value(res, res_std);
	return same_mem(dest_std, dest, MEM_SIZE) && result;
}

int test_strlcpy(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	res = single_test_strlcpy(dest, dest_std, "aaa", 0) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 2) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 3) && res;
	res = single_test_strlcpy(dest, dest_std, "aaa", 4) && res;
	res = single_test_strlcpy(dest, dest_std, "aasdjj;s;sa", 100) && res;
	return res;
}
#endif

#ifdef TEST_STRLCPY
int single_test_strlcat(char *dest, char *dest_std, char *orig, char *src, int n)
{
	int result = 1;

	sprintf(function, "ft_strlcat(\"%s\", \"%s\", %i)", orig, src, n);
	reset_with(dest, dest_std, orig, MEM_SIZE);

	int res = ft_strlcat(dest, src, n);
	int res_std = strlcat(dest_std, src, n);
	result = same_value(res, res_std);
	return same_mem(dest_std, dest, MEM_SIZE) && result;
}

int test_strlcat(void)
{
	char dest[MEM_SIZE];
	char dest_std[MEM_SIZE];

	int res = 1;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 0) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 1) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 2) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 3) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 4) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 5) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 6) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 7) && res;
	res = single_test_strlcat(dest, dest_std, "pqrstuvwxyz", "abcd", 20) && res;
	res = single_test_strlcat(dest, dest_std, "pqrs", "abcdefghi", 20) && res;
	return res;
}
#endif

#ifdef TEST_STRCHR
int single_test_strchr(char *str, int ch)
{
	sprintf(function, "ft_strchr(%p: \"%s\", %s)", str, str, escape_chr(ch));
	char *res = ft_strchr(str, ch);
	char *res_std = strchr(str, ch);

	return same_ptr(res, res_std);
}

int test_strchr(void)
{
	int res = 1;

	res = single_test_strchr("teste", 't') && res;
	res = single_test_strchr("teste", 'e') && res;
	res = single_test_strchr("teste", '\0') && res;
	res = single_test_strchr("teste", 'a') && res;

	return res;
}
#endif

#ifdef TEST_STRRCHR
int single_test_strrchr(char *str, int ch)
{
	sprintf(function, "ft_strrchr(%p: \"%s\", %s)", str, str, escape_chr(ch));
	char *res = ft_strrchr(str, ch);
	char *res_std = strrchr(str, ch);

	return same_ptr(res, res_std);
}

int test_strrchr(void)
{
	int res = 1;

	res = single_test_strrchr("teste", 'e') && res;
	res = single_test_strrchr("teste", '\0') && res;
	res = single_test_strrchr("xteste", 'x') && res;
	res = single_test_strrchr("teste", 'x') && res;

	res = single_test_strrchr("teste", 1024 + 'e') && res;

	return res;
}
#endif

#ifdef TEST_STRNCMP
int single_test_strncmp(char *str1, char *str2, size_t n)
{
	sprintf(function, "ft_strncmp(\"%s\", \"%s\", %lu)", escape_str(str1), escape_str(str2), n);
	int res = ft_strncmp(str1, str2, n);
	int res_std = strncmp(str1, str2, n);

	return same_sign(res, res_std);
}

int test_strncmp(void)
{
	int res = 1;

	res = single_test_strncmp("teste", "teste", 0) && res;
	res = single_test_strncmp("teste", "teste", 1) && res;
	res = single_test_strncmp("teste", "teste", 5) && res;
	res = single_test_strncmp("teste", "teste", 6) && res;
	res = single_test_strncmp("teste", "teste", 7) && res;
	res = single_test_strncmp("teste", "testex", 6) && res;
	res = single_test_strncmp("teste", "test", 10) && res;
	res = single_test_strncmp("test", "teste", 10) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_strncmp((char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_strncmp((char *)s1, (char *)s2, 7);
	if (!other) {
		printf(RED "You are not stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}
#endif

#ifdef TEST_MEMCHR
int single_test_memchr(char *str, int ch)
{
	sprintf(function, "ft_memchr(%p, 0x%X)", str, ch);
	char *res = ft_strchr(str, ch);
	char *res_std = strchr(str, ch);

	int result = same_ptr(res, res_std);
	if (!result) {
		print_mem_full(str, 0x30);
	}
	return result;
}

int test_memchr(void)
{
	int res = 1;
	char str[100];

	for (int i = 0; i < REPETITIONS && res; i++) {
		res = single_test_memchr(rand_bytes(str, 0x31), rand() % 0x200) && res;
	}
	return res;
}
#endif


#ifdef TEST_MEMCMP
int single_test_memcmp(char *str1, char *str2, size_t n)
{
	sprintf(function, "ft_memcmp(\"%s\", \"%s\", %lu)", escape_str(str1), escape_str(str2), n);
	int res = ft_memcmp(str1, str2, n);
	int res_std = memcmp(str1, str2, n);

	return same_sign(res, res_std);
}

int test_memcmp(void)
{
	int res = 1;

	res = single_test_memcmp("teste", "teste", 0) && res;
	res = single_test_memcmp("teste", "teste", 1) && res;
	res = single_test_memcmp("teste", "teste", 5) && res;
	res = single_test_memcmp("teste", "teste", 6) && res;
	res = single_test_memcmp("teste", "testex", 6) && res;
	res = single_test_memcmp("teste", "test", 10) && res;
	res = single_test_memcmp("test", "teste", 10) && res;

	unsigned char s1[10] = "abcdef";
	unsigned char s2[10] = "abc\xfdxx";
	res = single_test_memcmp((char *)s1, (char *)s2, 5) && res;

	s1[3] = 0;
	s2[3] = 0;
	int other = single_test_memcmp((char *)s1, (char *)s2, 7);
	if (!other) {
		printf(RED "You are stoping at the '\\0'\n" NC);
		res = 0;
	}
	return res;
}
#endif

void handler(int nSignum, struct __siginfo *a, void *b)
{
	nSignum = 3;
	a = (struct __siginfo *)b;
	printf("%-10s: " RED "Segmentation Fault!" RED, function);
	exit(EXIT_FAILURE);
}

int main()
{
	struct sigaction action;
	memset(&action, 0, sizeof(struct sigaction));
	action.sa_flags = SA_SIGINFO;
	action.sa_sigaction = handler;
	sigaction(SIGSEGV, &action, NULL);

	test(isalpha);
	test(isdigit);
	test(isalnum);
	test(isascii);
	test(isprint);
	test(toupper);
	test(tolower);

	test(memset);
	test(bzero);
	test(memcpy);
	test(memmove);
	test(memchr);
	test(memcmp);

	test(strlen);
	test(strlcpy);
	test(strlcat);
	test(strchr);
	test(strrchr);
	test(strncmp);

	return 0;
}
