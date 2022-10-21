
#include "../libft.h"

void f(void *ptr) {}

void d(void *ptr) {}

int main() {
	t_list *l = NULL;
	ft_lstmap(l, f, d);
}