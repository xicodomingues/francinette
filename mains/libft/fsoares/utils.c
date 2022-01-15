#include "utils.h"

int where_buffer = 0;

void handler(int nSignum, struct __siginfo *a, void *b)
{
	nSignum = 3;
	a = (struct __siginfo *)b;
	printf("%-10s: " RED "Segmentation Fault!\n" NC, function);
	exit(EXIT_FAILURE);
}

void set_sigsev()
{
	struct sigaction action;
	memset(&action, 0, sizeof(struct sigaction));
	action.sa_flags = SA_SIGINFO;
	action.sa_sigaction = handler;
	sigaction(SIGSEGV, &action, NULL);
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
			printf(i % 2 ? "   " : "  ");
	int limit = (size == -1 ? 16 : size);
	int i = 0;
	while (i < limit)
	{
		printf("%c", isprint(ptr[i]) ? ptr[i] : '.');
		i++;
	}
	printf("\n");
}

void print_mem_full(void *ptr, int size)
{
	if (ptr == NULL || ptr == 0)
	{
		printf("ERROR: %p points to NULL\n", ptr);
		return;
	}
	int i = 0;
	unsigned char *ptrc = ptr;
	while (i < size)
	{
		if (i % 16 == 0)
		{
			if (is_empty(ptr + i)) {
				i += 16;
				continue;
			}
			printf("%p: ", ptr + i);
		}
		printf("%02x%s", ptrc[i], (i % 2 ? " " : ""));
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
		printf("ERROR: %p points to NULL\n", ptr);
		return;
	}
	int i = 0;
	unsigned char *ptrc = ptr;
	while (i < size)
	{
		if (i % 16 == 0)
		{
			if (is_empty(ptr + i)) {
				i += 16;
				continue;
			}
			printf("%04x: ", i);
		}
		printf("%02x%s", ptrc[i], (i % 2 ? " " : ""));
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

int error(const char *format, ...)
{
	printf(RED "Error" NC ": " CYN "%s" NC ": ", function);
	va_list args;
	va_start(args, format);
	vprintf(format, args);
	va_end(args);
	return 0;
}

int same_ptr(void *res, void *res_std)
{
	if (res != res_std)
		return error("yours: %p, std: %p\n", res, res_std);
	return 1;
}

int same_mem(void *s, void *r, int size)
{
	int equal = 1;
	char *std = s;
	char *res = r;
	for (int i = 0; i < size; i++)
		if (std[i] != res[i])
			equal = 0;
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
		return error("yours: %i, std: %i\n", res, res_std);
	return 1;
}

int same_sign(int res, int res_std)
{
	int rs = (res > 0 ? 1 : (res < 0 ? -1 : 0));
	int rss = (res_std > 0 ? 1 : (res_std < 0 ? -1 : 0));
	if (rs != rss)
		return error("yours: %i (%i), std: %i (%i)\n", rs, res, rss, res_std);
	return 1;
}

int same_offset(void *start, void *start_std, void *res, void *res_std)
{
	long diff = (long)res - (long)start;
	long diff_std = (long)res_std - (long)start_std;

	if (res == NULL && res_std == NULL)
		return 1;
	if (diff == diff_std)
		return 1;
	if ((res == NULL && res_std != NULL) || (res != NULL && res_std == NULL))
		return error("yours: %p, std: %p\n");

	return error("offset: yours: %i, std: %i\n", diff, diff_std);
}

int same_return(void *res, void *dest)
{
	if (res != dest)
	{
		return error("should return: %p, but returned: %p", dest, res);
	}
	return 1;
}
