#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

int server_pid;
int signals_val[1000000];
int signals_source[1000000];
int signal_pos = 0;
FILE *outfile;

void sighandler(int signum, int c_pid)
{
	static int client_pid = -1;
	if (signum == 2 && c_pid != server_pid && c_pid != client_pid)
	{
		for (size_t i = 0; i < signal_pos; i++)
			printf("%i from %i\n", signals_val[i], signals_source[i]);
		printf("\n=====\n");
		exit(0);
	}

	signals_val[signal_pos] = signum;
	signals_source[signal_pos++] = c_pid;
	if (c_pid != server_pid && client_pid == -1)
	{
		fprintf(outfile, "setting client to: %i\n", c_pid);
		client_pid = c_pid;
	}
	if (c_pid == client_pid) {
		//fprintf(outfile, "sending %i to server %i\n", signum, server_pid);
		kill(server_pid, signum);
	}
	else if (c_pid == server_pid) {
		//fprintf(outfile, "sending %i to client %i\n", signum, client_pid);
		kill(client_pid, signum);
	}
}

void get_pid(int signum, siginfo_t *info, void *context)
{
	if (context)
		sighandler(signum, info->si_pid);
}

int main(int argc, char *argv[])
{
	struct sigaction sa;

	outfile = fopen("signals_middle.log", "w");
	printf("__PID: %i\n-----\n", getpid());
	server_pid = atoi(argv[1]);
	sa.sa_flags = SA_SIGINFO;
	sa.sa_sigaction = get_pid;
	for (int sig = 1; sig < NSIG; sig++)
		sigaction(sig, &sa, NULL);
	while (1)
		sleep(1);
	return (0);
}