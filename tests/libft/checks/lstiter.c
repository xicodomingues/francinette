
#include "../libft.h"

void f(void *ptr) {}

int main() {
	t_list *l = NULL;
	ft_lstiter(l, f);
}