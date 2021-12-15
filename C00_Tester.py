from CommonTester import CommonTester


class C00_Tester(CommonTester):

    def ex00(self):
        # The files that you should deliver in the git repo
        self.exercise_files = ["ft_putchar.c"]
        # The files that compose the test
        self.test_files = ["main.c"]
        # by default it uses: -Wall -Wextra -Werror, if you define the variable bellow
        # it will use these flags instead
        # self.compile_flags = ["-Wall", "-Wextra"]

    def ex01(self):
        self.exercise_files = ["ft_print_alphabet.c"]
        self.test_files = ["main.c"]

    def ex02(self):
        self.exercise_files = ["ft_print_reverse_alphabet.c"]
        self.test_files = ["main.c"]

    def ex03(self):
        self.exercise_files = ["ft_print_numbers.c"]
        self.test_files = ["main.c"]

    def ex04(self):
        self.exercise_files = ["ft_is_negative.c"]
        self.test_files = ["main.c"]

    def ex05(self):
        self.exercise_files = ["ft_print_comb.c"]
        self.test_files = ["main.c"]

    def ex06(self):
        self.exercise_files = ["ft_print_comb2.c"]
        self.test_files = ["main.c"]

    def ex07(self):
        self.exercise_files = ["ft_putnbr.c"]
        self.test_files = ["main.c"]

    def ex08(self):
        self.exercise_files = ["ft_print_combn.c"]
        self.test_files = ["main.c"]
