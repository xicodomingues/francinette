from CommonTester import CommonTester


class C02_Tester(CommonTester):

    def ex00(self):
        self.exercise_files = ["ft_strcpy.c"]
        self.test_files = ["main.c"]

    def ex01(self):
        self.exercise_files = ["ft_strncpy.c"]
        self.test_files = ["main.c"]

    def ex02(self):
        self.exercise_files = ["ft_str_is_alpha.c"]
        self.test_files = ["main.c"]

    def ex03(self):
        self.exercise_files = ["ft_str_is_numeric.c"]
        self.test_files = ["main.c"]

    def ex04(self):
        self.exercise_files = ["ft_str_is_lowercase.c"]
        self.test_files = ["main.c"]

    def ex05(self):
        self.exercise_files = ["ft_str_is_uppercase.c"]
        self.test_files = ["main.c"]

    def ex06(self):
        self.exercise_files = ["ft_str_is_printable.c"]
        self.test_files = ["main.c"]

    def ex07(self):
        self.exercise_files = ["ft_strupcase.c"]
        self.test_files = ["main.c"]

    def ex08(self):
        self.exercise_files = ["ft_strlowcase.c"]
        self.test_files = ["main.c"]

    def ex09(self):
        self.exercise_files = ["ft_strcapitalize.c"]
        self.test_files = ["main.c"]

    def ex10(self):
        self.exercise_files = ["ft_strlcpy.c"]
        self.test_files = ["main.c"]

    def ex11(self):
        self.exercise_files = ["ft_putstr_non_printable.c"]
        self.test_files = ["main.c"]

    def ex12(self):
        self.exercise_files = ["ft_print_memory.c"]
        self.test_files = ["main.c"]
