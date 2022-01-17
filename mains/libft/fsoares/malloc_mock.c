#define _GNU_SOURCE
#include <dlfcn.h>

#include "utils.h"

char malloc_ptr_info[10000];
size_t position;
void *results[100];
int res_pos = 0;
int cur_res_pos = 0;


static void save_ptr(void *ptr, size_t size, void *to_return)
{
	char *where = (char *)(malloc_ptr_info + position);
	int len = sprintf(where, "%p:%zu:%p|", ptr, size, to_return);
	position += len;
}

void * malloc(size_t size)
{
    void *(*libc_malloc)(size_t) = (void *(*)(size_t))dlsym(RTLD_NEXT, "malloc");
    void *p = libc_malloc(size);
	void *to_return = p;
	if (res_pos > cur_res_pos)
		to_return = results[cur_res_pos++];
    save_ptr(p, size, to_return);
    return (to_return);
}

void free(void * p)
{
    void (*libc_free)(void*) = (void (*)(void *))dlsym(RTLD_NEXT, "free");
    libc_free(p);
}

void reset_malloc_mock()
{
	res_pos = 0;
	cur_res_pos = 0;
	position = 0;
}

void malloc_set_result(void *res) {
	results[res_pos++] = res;
}

size_t get_malloc_size(void *ptr)
{
	char pointer[20];

	sprintf(pointer, "%p:", ptr);
	char *found = strstr(malloc_ptr_info, pointer);
	if (found == NULL)
		return 0;
	char *size = strchr(found, ':');
	return atoi(size + 1);
}

void malloc_show_inner_str()
{
	printf("%s\n", malloc_ptr_info);
}