from CommonTester import CommonTester


class C00_Tester(CommonTester):

    def ex00(self):
        # which files are needed to compile the program
        self.compile = ["main.c", "ft_putchar.c"]
        # which files you want norminette to ignore
        self.norm_ignore = ["main.c"]
        # by default it uses: -Wall -Wextra -Werror, if you define the variable bellow
        # it will use these flags instead
        # self.compile_flags = ["-Wall", "-Wextra"]

    def ex01(self):
        self.compile = ["main.c", "ft_print_alphabet.c"]
        self.norm_ignore = ["main.c"]

    def ex02(self):
        self.compile = ["main.c", "ft_print_reverse_alphabet.c"]
        self.norm_ignore = ["main.c"]