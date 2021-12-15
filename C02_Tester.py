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

