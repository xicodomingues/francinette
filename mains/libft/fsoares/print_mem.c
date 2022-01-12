#include <stdio.h>
#include <ctype.h>

static void print_str(unsigned char *ptr, int size) {
  if (size != -1) {
    for (int i = size % 16; i < 16; i++) {
      printf(i % 2 ? "   " : "  ");
    }
  }
  int limit = (size == -1 ? 16 : size);
  int i = 0;
  while (i < limit) {
    printf("%c", isalnum(ptr[i]) ? ptr[i] : '.');
    i++;
  }
  printf("\n");
}

void print_mem(void *ptr, int size) {
  if (ptr == NULL || ptr == 0) {
    printf("ERROR: %p points to NULL\n", ptr);
    return;
  }
  int i = 0;
  unsigned char *ptrc = ptr;
  while (i < size) {
    if (i % 16 == 0) {
      printf("%04x: ", i);
    }
    printf("%02x%s", ptrc[i], (i % 2 ? " " : ""));
    i++;
    if (i % 16 == 0) {
      print_str(ptrc + i - 16, -1);
    }
  }
  if (i % 16 != 0) {
    print_str(ptrc + i - i % 16, i % 16);
  }
}