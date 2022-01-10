.DEFAULT_GOAL	:= a
UTILS			= $(addprefix utils/, sigsegv.cpp color.cpp check.cpp leaks.cpp)
PARENT_DIR		= $(shell dirname $(shell pwd))
LIBFT_PATH		= $(PARENT_DIR)
TESTS_PATH		= tests/
MANDATORY		= memset bzero memcpy memmove memchr memcmp strlen isalpha isdigit isalnum \
				isascii isprint toupper tolower strchr strrchr strncmp strlcpy strlcat strnstr \
				atoi calloc strdup substr strjoin strtrim split itoa strmapi putchar_fd putstr_fd \
				putendl_fd putnbr_fd striteri
BONUS			= lstnew lstadd_front lstsize lstlast lstadd_back lstdelone lstclear lstiter lstmap
VSOPEN			= $(addprefix vs, $(MANDATORY)) $(addprefix vs, $(BONUS))

CC		= clang++
CFLAGS	= -g3 -ldl -std=c++11 -I utils/ -I$(LIBFT_PATH) 
UNAME = $(shell uname -s)
ifeq ($(UNAME), Linux)
	VALGRIND = valgrind -q --leak-check=full
endif
ifeq ($(IN_DOCKER),TRUE)
	LIBFT_PATH = /project/
endif

$(MANDATORY): %: mandatory_start
	@$(CC) $(CFLAGS) $(UTILS) $(TESTS_PATH)ft_$*_test.cpp -L$(LIBFT_PATH) -lft && $(VALGRIND) ./a.out && rm -f a.out

$(BONUS): %: bonus_start
	@$(CC) $(CFLAGS) $(UTILS) $(TESTS_PATH)ft_$*_test.cpp -L$(LIBFT_PATH) -lft && $(VALGRIND) ./a.out && rm -f a.out

$(VSOPEN): vs%:
	@code $(TESTS_PATH)ft_$*_test.cpp

mandatory_start: update message
	@tput setaf 6
	make -C $(LIBFT_PATH)
	@tput setaf 4 && echo [Mandatory]

bonus_start: update message
	@tput setaf 6
	make bonus -C $(LIBFT_PATH)
	@tput setaf 5 && echo [Bonus]

update:
	@git pull

message: checkmakefile
	@tput setaf 3 && echo "If all your tests are OK and the moulinette KO you, please run the tester with valgrind (see README)"

checkmakefile:
	@ls $(LIBFT_PATH) | grep Makefile > /dev/null 2>&1 || (tput setaf 1 && echo Makefile not found. && exit 1)

$(addprefix docker, $(MANDATORY)) $(addprefix docker, $(BONUS)) dockerm dockerb dockera: docker%:
	@docker rm -f mc > /dev/null 2>&1 || true
	docker build -qt mi .
	docker run -e IN_DOCKER=TRUE -dti --name mc -v $(LIBFT_PATH):/project/ -v $(PARENT_DIR)/libftTester:/project/libftTester mi
	docker exec -ti mc make $* -C libftTester || true
	@docker rm -f mc > /dev/null 2>&1

m: $(MANDATORY)
b: $(BONUS)
a: m b 

clean:
	make clean -C $(LIBFT_PATH) && rm -rf a.out*

fclean:
	make fclean -C $(LIBFT_PATH) && rm -rf a.out*

.PHONY:	mandatory_start m bonus_start b a fclean clean update message $(VSOPEN) $(MAIL)
