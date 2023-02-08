#ifndef LIST_UTILS_H
#define LIST_UTILS_H

#include "my_utils.h"

int same_list_elem(t_list *expected, t_list *result);

t_list *lstnew(void *content);
void lstadd_front(t_list **list, t_list *new);
t_list **create_list(int n_elems, ...);
int same_list(t_list **expected, t_list **result);
int same_list_bool(t_list **expected, t_list **result);

char *node_to_str(t_list *node);
char *list_to_str(t_list **head_ptr);
char *list_to_str_fn(t_list **head_ptr, char *(*str_node)(t_list *node));
t_list *lstlast(t_list *lst);
void lstadd_back(t_list **list, t_list *new);
void lstclear(t_list **lst, void (*del)(void *));

#endif