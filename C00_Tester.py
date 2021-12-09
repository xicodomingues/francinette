from CommonTester import CommonTester


C00_BASE_DIR = '/path/to/your/base/c00/where/inside/you/have/the/ex0X'
C00_TEST_FILES_DIR = '/path/to/where/your/mains/and/expected/are'


class C00_Tester(CommonTester):

    def ex00(self):
        # which files are needed to compile the program
        self.compile = ["main.c", "ft_putchar.c"]
        # which files you want norminette to ignore
        self.norm_ignore = ["main.c"]

    def ex01(self):
        self.compile = ["main.c", "ft_print_alphabet.c"]
        self.norm_ignore = ["main.c"]

