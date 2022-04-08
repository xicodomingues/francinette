
all:
	@gcc middleman.c -o middleman.out
	@make -s -C ../__my_srcs all > /dev/null

bonus:
	@gcc middleman.c -o middleman.out
	@make -s -C ../__my_srcs bonus > /dev/null
	@if [ -f ../__my_srcs/client_bonus ]; then mv ../__my_srcs/client_bonus ../__my_srcs/client; fi;
	@if [ -f ../__my_srcs/server_bonus ]; then mv ../__my_srcs/server_bonus ../__my_srcs/server; fi;

fclean:
	@make -s -C ../__my_srcs fclean > /dev/null
