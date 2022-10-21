#define _GNU_SOURCE
#include <dlfcn.h>
#include <execinfo.h>

#include "utils.h"

char function[1000];
char signature[100000];
int g_offset;
char escaped[100000];
char escaped_div = 5;
int where_buffer = 0;
int g_test = 1;
int child_pid = -1;

FILE *errors_file;

void show_timeout()
{
	fprintf(errors_file, BRED "Error" NC " in test %i: " CYN "%s" NC ": " BRED "%s" NC "\n",
			g_test, signature, ("Timeout occurred. You can increase the timeout by executing " BWHT "francinette --timeout <number of seconds>" NC));
	printf(YEL "%i.KO %s\n" NC, g_test++, "TIMEOUT");
}

void show_signal_msg(char *message, char *resume, int signal)
{
	if (child_pid != -1)
	{
		kill(child_pid, SIGKILL);
		child_pid = -1;
		printf("\b");
	}
	fprintf(errors_file, BRED "Error" NC " in test %i: " CYN "%s" NC ": " BRED "%s"NC"\n",
			g_test, signature, message);

#ifdef __APPLE__
	if (signal != SIGALRM)
	{
		void *buffer[20];
		int nptrs = backtrace(buffer, 20);
		char **strings = backtrace_symbols(buffer, nptrs);
		save_traces(strings, nptrs);
	}
#endif

	printf(YEL "%i.KO %s\n" NC, g_test++, resume);
	exit(signal);
}

void sigsegv(int signal)
{
	show_signal_msg("Segmentation fault!", "Segfault", signal);
}

void sigabort(int signal)
{
	show_signal_msg("Memory problems!", "Abort", signal);
}

void sigbus(int signal)
{
	show_signal_msg("Bus error: Trying to set unwritable memory", "Bus Error", signal);
}

void sigalarm(int signal)
{
	show_signal_msg(("Timeout occurred. You can increase the timeout by executing " BWHT "francinette --timeout <number of seconds>" NC), "Timeout", signal);
}

void handle_signals()
{
	signal(SIGSEGV, sigsegv);
	signal(SIGABRT, sigabort);
	signal(SIGBUS, sigbus);
	signal(SIGALRM, sigalarm);
	srand((unsigned int)time(NULL));
	srandom((unsigned int)time(NULL));
}

void setup_framework(int argn, char **argv)
{
	(void)argn;
	handle_signals();
	FILE *final_file = fopen("error_color.log", "a");
	fprintf(final_file, "##==##==##&&##==##==##%s\n", argv[0]);
}

int show_res(int res, char *prefix)
{
	if (!res)
		printf(RED "%i%s.KO " NC, g_test++, prefix);
	else
		printf(GRN "%i%s.OK " NC, g_test++, prefix);
	fflush(stdout);
	return res;
}

static int is_empty(unsigned char *p)
{
	for (int i = 0; i < 16; i++)
		if (p[i] != 0x11)
			return 0;
	return 1;
}

static void print_str(unsigned char *ptr, int size)
{
	if (size != -1)
		for (int i = size % 16; i < 16; i++)
			fprintf(errors_file, i % 2 ? "   " : "  ");
	int limit = (size == -1 ? 16 : size);
	int i = 0;
	fprintf(errors_file, "->  ");
	while (i < limit)
	{
		fprintf(errors_file, "%c", isprint(ptr[i]) ? ptr[i] : '.');
		i++;
	}
	fprintf(errors_file, "\n");
}

void print_mem_full(void *ptr, int size)
{
	if (ptr == NULL || ptr == 0)
	{
		fprintf(errors_file, "ERROR: %p points to NULL\n", ptr);
		return;
	}
	int i = 0;
	unsigned char *ptrc = ptr;
	while (i < size)
	{
		if (i % 16 == 0)
		{
			if (is_empty(ptr + i))
			{
				i += 16;
				continue;
			}
			fprintf(errors_file, "at 0x%p: ", ptr + i);
		}
		fprintf(errors_file, "%02x%s", ptrc[i], (i % 2 ? " " : ""));
		i++;
		if (i % 16 == 0)
		{
			print_str(ptrc + i - 16, -1);
		}
	}
	if (i % 16 != 0)
	{
		print_str(ptrc + i - i % 16, i % 16);
	}
}

void print_mem(void *ptr, int size)
{
	if (ptr == NULL || ptr == 0)
	{
		fprintf(errors_file, "ERROR: %p points to NULL\n", ptr);
		return;
	}
	int i = 0;
	unsigned char *ptrc = ptr;
	while (i < size)
	{
		if (i % 16 == 0)
		{
			if (is_empty(ptr + i) && i > 0)
			{
				i += 16;
				continue;
			}
			fprintf(errors_file, "%04x: ", i);
		}
		fprintf(errors_file, "%02x%s", ptrc[i], (i % 2 ? " " : ""));
		i++;
		if (i % 16 == 0)
		{
			print_str(ptrc + i - 16, -1);
		}
	}
	if (i % 16 != 0)
	{
		print_str(ptrc + i - i % 16, i % 16);
	}
}

char *rand_bytes(char *dest, int len)
{
	dest[len - 1] = '\0';
	for (int i = 0; i < len - 1; i++)
	{
		dest[i] = rand() % 0x100;
	}
	return dest;
}

char *rand_str(char *dest, int len)
{
	dest[len - 1] = '\0';
	for (int i = 0; i < len - 1; i++)
	{
		dest[i] = rand() % ('~' - ' ') + ' ';
	}
	return dest;
}

char *truncate_str(char *src)
{
	char temp[1000];

	int len = strlen(src);
	temp[0] = '"';
	strncpy(temp + 1, src, 21);
	strncpy(temp + 21, "[...]", 6);
	strncpy(temp + 26, src + len - 20, 21);
	sprintf(temp + 46, "\"(%i characters)", len);
	char *res = escape_str(temp);
	len = strlen(res);
	res[len - 1] = '\0';
	return res + 1;
}

char *escape_str(char *src)
{
	int i, j;
	where_buffer = (where_buffer + 1) % escaped_div;
	char *my_bf = escaped + where_buffer * (100000 / escaped_div);
	if (src == NULL)
	{
		sprintf(my_bf, "<NULL>");
		return my_bf;
	}
	if (strlen(src) > 100)
		return truncate_str(src);

	my_bf[0] = '"';
	for (i = 0, j = 1; src[i]; i++, j++)
	{
		if (isprint(src[i]))
			my_bf[j] = src[i];
		else if (src[i] == '\n')
			sprintf(my_bf + j++, "\\n");
		else if (src[i] == '\t')
			sprintf(my_bf + j++, "\\t");
		else if (src[i] == '\f')
			sprintf(my_bf + j++, "\\f");
		else if (src[i] == '\r')
			sprintf(my_bf + j++, "\\r");
		else if (src[i] == '\v')
			sprintf(my_bf + j++, "\\v");
		else
		{
			sprintf(my_bf + j, "\\%03o", (unsigned char)src[i]);
			j += 3;
		}
	}
	my_bf[j] = '"';
	my_bf[j + 1] = '\0';
	return my_bf;
}

char *escape_chr(char ch)
{
	if (ch == '\0')
	{
		return "'\\0'";
	}
	else
	{
		char to_escape[20] = "' '";
		to_escape[1] = ch;
		char *res = escape_str(to_escape);
		size_t len = strlen(res);
		res[len - 1] = '\0';
		return res + 1;
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

int set_signature(const char *format, ...)
{
	va_list args;
	va_start(args, format);
	g_offset = vsprintf(signature, format, args);
	va_end(args);
	return g_offset;
}

int error(const char *format, ...)
{
	fprintf(errors_file, BRED "Error" NC " in test %i: " CYN "%s" NC ": ", g_test, signature);
	va_list args;
	va_start(args, format);
	vfprintf(errors_file, format, args);
	va_end(args);
	return 0;
}

void add_to_error_file()
{
	char buf[1024];
	fclose(errors_file);

	FILE *file, *final_file;
	size_t nread;
	file = fopen("errors.log", "r");
	final_file = fopen("error_color.log", "a");
	if (file && final_file)
	{
		while ((nread = fread(buf, 1, sizeof buf, file)) > 0)
			fwrite(buf, 1, nread, final_file);
		if (ferror(file))
		{
			fprintf(final_file, "\nProblem reading error output file");
		}
		if (ferror(final_file))
		{
			printf("\nProblem appending output to error file.n");
		}
		fseek(final_file, -2, SEEK_END);
		nread = fread(buf, 1, sizeof buf, final_file);
		if (nread == 2)
		{
			if(buf[0] != '\n')
			{
				fwrite("\n", 1, 1, final_file);
			}
			if (buf[1] != '\n')
				fwrite("\n\n", 1, 2, final_file);
		}
		fclose(file);
		fclose(final_file);
	}
}

int same_ptr(void *res, void *res_std)
{
	unsigned long bytes = (unsigned long)res;
	unsigned long bytes_std = (unsigned long)res_std;
	bytes &= 0xFFFFFFFFl;
	bytes_std &= 0xFFFFFFFFl;
	if (bytes != bytes_std)
		return error("yours: %p, std: %p\n", bytes, bytes_std);
	return 1;
}

int same_mem(void *expected, void *result, int size)
{
	int equal = 1;
	char *std = expected;
	char *res = result;
	for (int i = 0; i < size; i++)
		if (std[i] != res[i])
			equal = 0;
	if (!equal)
	{
		error("different memory" NC "\n");
		fprintf(errors_file, YEL "expected" NC ":\n");
		print_mem(std, size);
		fprintf(errors_file, YEL "yours" NC ":\n");
		print_mem(res, size);
		fprintf(errors_file, "\n");
	}
	return equal;
}

int same_value(int expected, int res)
{
	if (res != expected)
		return error("expected: %i, yours: %i\n", expected, res);
	return 1;
}

int same_return_value(int expected, int res)
{
	if (res != expected)
		return error("returned: %i, but expected: %i\n", res, expected);
	return 1;
}

int same_sign(int expected, int res)
{
	int expected_sign = (expected > 0 ? 1 : (expected < 0 ? -1 : 0));
	int res_sign = (res > 0 ? 1 : (res < 0 ? -1 : 0));
	if (expected_sign != res_sign)
		return error("\nexpected sign: %i (value: %i), yours sign: %i (value: %i)\n\n", expected_sign, expected, res_sign, res);
	return 1;
}

int same_offset(void *expected_start, void *expected_res, void *start, void *res)
{
	long offset = (long)res - (long)start;
	long expected_offset = (long)expected_res - (long)expected_start;

	if (res == NULL && expected_res == NULL)
		return 1;
	if (offset == expected_offset)
		return 1;
	if ((res == NULL && expected_res != NULL) || (res != NULL && expected_res == NULL))
		return error("expected: %p, yours: %p\n", expected_res, res);

	return error("\nexpected: %p (offset %i), yours: %p (offset %i)\n\n",
				 expected_res, expected_offset, res, offset);
}

int same_return(void *expected, void *res)
{
	if (expected != res)
	{
		return error("should return: %p, but returned: %p", expected, res);
	}
	return 1;
}

int same_string(char *expected, char *actual)
{
	if (expected == NULL && actual == NULL)
		return 1;
	if ((expected == NULL && actual != NULL) || (expected != NULL && actual == NULL))
	{
		return error("expected: %s, got: %s\n", escape_str(expected), escape_str(actual));
	}
	if (strcmp(expected, actual) != 0)
	{
		return error("expected: %s, got: %s\n", escape_str(expected), escape_str(actual));
	}
	return 1;
}

int check_mem_size(void *ptr, size_t expected_size)
{
	size_t res = get_malloc_size(ptr);

#ifdef STRICT_MEM
	char *message = "expected %zu bytes, allocated %zu bytes\n";
	if (expected_size != res)
#else
	char *message = "not enough memory allocated, needed: %zu, reserved: %zu\n";
	if (expected_size > res)
#endif
	{
		error(message, expected_size, res);
		show_malloc_stack(ptr);
		return 0;
	}
	return 1;
}

char *my_strdup(const char *s1)
{
	return (my_strndup(s1, strlen(s1) + 1));
}

char *my_strndup(const char *s1, size_t size)
{
	size_t len;
	char *result;

	len = strlen(s1);
	if (size < len)
		len = size;
	result = (char *)malloc(1 + len * sizeof(char));
	if (result == NULL)
		return (result);
	strlcpy(result, s1, len + 1);
	result[len] = 0;
	return (result);
}

#ifndef __APPLE__

size_t strlcat(char *dst, const char *src, size_t dsize)
{
	const char *odst = dst;
	const char *osrc = src;
	size_t n = dsize;
	size_t dlen;

	while (n-- != 0 && *dst != '\0')
		dst++;
	dlen = dst - odst;
	n = dsize - dlen;

	if (n-- == 0)
		return (dlen + strlen(src));
	while (*src != '\0')
	{
		if (n != 0)
		{
			*dst++ = *src;
			n--;
		}
		src++;
	}
	*dst = '\0';

	return (dlen + (src - osrc));
}

size_t strlcpy(char *dst, const char *src, size_t dsize)
{
	const char *osrc = src;
	size_t nleft = dsize;

	if (nleft != 0)
	{
		while (--nleft != 0)
			if ((*dst++ = *src++) == '\0')
				break;
	}
	if (nleft == 0)
	{
		if (dsize != 0)
			*dst = '\0';
		while (*src++)
			;
	}

	return (src - osrc - 1);
}

char *strnstr(const char *s1, const char *s2, size_t n)
{
	size_t i, len;
	char c = *s2;

	if (c == '\0')
		return (char *)s1;

	for (len = strlen(s2); len <= n && *s1; n--, s1++)
	{
		if (*s1 == c)
		{
			for (i = 1;; i++)
			{
				if (i == len)
					return (char *)s1;
				if (s1[i] != s2[i])
					break;
			}
		}
	}
	return NULL;
}

#endif
