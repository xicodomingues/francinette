
#include "../libft.h"

void d(void *ptr) {}

int main() {
	t_list *l = NULL;
	ft_lstclear(l, d);
}