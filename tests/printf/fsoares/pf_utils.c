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