#define _GNU_SOURCE  
#include <stdio.h>

#include "pf_utils.h"
#include <execinfo.h>

void cout(const char *f, ...)
{
	va_list ap;

	if (output_fd == -1)
		output_fd = open("/dev/tty", O_RDWR);

	va_start(ap, f);
	vdprintf(output_fd, f, ap);
	va_end(ap);
}

int show_result(int res, char *prefix)
{
	if (!res)
		cout(RED "%i.KO%s " NC, g_test++, prefix);
	else
		cout(GRN "%i.OK%s " NC, g_test++, prefix);
	fflush(stdout);
	return res;
}

void pf_show_timeout()
{
	fprintf(errors_file, BRED "Error" NC " in test %i: " CYN "%s" NC ": " BRED "%s" NC "\n",
			g_test, signature, ("Timeout occurred. You can increase the timeout by executing " BWHT "francinette --timeout <number of seconds>" NC));
	cout(YEL "%i.KO %s\n" NC, g_test++, "TIMEOUT");
}

void pf_show_signal_msg(char *message, char *resume, int signal)
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

	cout(YEL "%i.KO %s\n" NC, g_test++, resume);
	exit(signal);
}

void pf_sigsegv(int signal)
{
	pf_show_signal_msg("Segmentation fault!", "Segfault", signal);
}

void pf_sigabort(int signal)
{
	pf_show_signal_msg("Memory problems!", "Abort", signal);
}

void pf_sigbus(int signal)
{
	pf_show_signal_msg("Bus error: Trying to set unwritable memory", "Bus Error", signal);
}

void pf_sigalarm(int signal)
{
	pf_show_signal_msg(("Timeout occurred. You can increase the timeout by executing " BWHT "francinette --timeout <number of seconds>" NC), "Timeout", signal);
}

void pf_handle_signals()
{
	signal(SIGSEGV, pf_sigsegv);
	signal(SIGABRT, pf_sigabort);
	signal(SIGBUS, pf_sigbus);
	signal(SIGALRM, pf_sigalarm);
	srand((unsigned int)time(NULL));
	srandom((unsigned int)time(NULL));
}

void pf_setup_framework(int argn, char **argv)
{
	(void)argn;
	pf_handle_signals();
	FILE *file_big = fopen("error_color.log", "a");
	fprintf(file_big, "##==##==##&&##==##==##%s\n", argv[0]);
}

#ifdef STRICT_MEM

#define WRITE_LIMIT 10000
t_node writes_saved[WRITE_LIMIT];
int write_count = 0;

typedef ssize_t (*t_write)(int, const void *ptr, size_t);

int write_fail = -1;

ssize_t write(int fd, const void *ptr, size_t len)
{
	t_write libc_write = (t_write)dlsym(RTLD_NEXT, "write");

	if (write_count < WRITE_LIMIT)
	{
		t_node new_node = writes_saved[write_count];
		void *buffer[20];
		int nptrs;
		char **strings;
		nptrs = backtrace(buffer, 20);
		strings = backtrace_symbols(buffer, nptrs);
		new_node.strings = strings;
		new_node.nptrs = nptrs;
		writes_saved[write_count] = new_node;
	}

	write_count++;
	if(write_count - 1 == write_fail)
		return (-1);
	return libc_write(fd, ptr, len);
}

int reset_write_count()
{
	int prev_count = write_count;
	write_fail = -1;
	write_count = 0;
	return prev_count > WRITE_LIMIT ? WRITE_LIMIT : prev_count;
}

void set_write_fail(int n)
{
	write_fail = n;
}

t_node *get_all_writes()
{
	t_node *result = calloc(write_count, sizeof(t_node));
	for (int i = 0; i < write_count; i++)
	{
		t_node temp;
		temp.nptrs = writes_saved[i].nptrs;
		temp.strings = calloc(temp.nptrs, sizeof(char *));
		for (int j = 0; j < temp.nptrs; j++)
			temp.strings[j] = strdup(writes_saved[i].strings[j]);
		result[i] = temp;
	}
	return result;
}

#endif
