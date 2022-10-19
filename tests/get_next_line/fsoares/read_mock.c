#include "file_utils.h"


ssize_t read(int fildes, void *buf, size_t nbyte)
{
	ssize_t(*libc_read)(int, void *, size_t) = 
		(ssize_t (*)(int, void *, size_t))dlsym(RTLD_NEXT, "read");
	if (nbyte != BUFFER_SIZE) {
		fprintf(errors_file, "Please use the read size provided by the compile variable BUFFER_SIZE: %i\n", BUFFER_SIZE);
		printf(RED "Use the fucking BUFFER_SIZE (%i), instead of what you wanted to read (%i)..." NC, BUFFER_SIZE, nbyte);
		exit(1);
	}
	return libc_read(fildes, buf, nbyte);
}
