from CommonTester import CommonTester


class C03_Tester(CommonTester):

    def ex00(self):
        self.exercise_files = ["ft_strlen.c"]
        self.test_files = ["main.c"]

    def ex01(self):
        self.exercise_files = ["ft_strncmp.c"]
        self.test_files = ["main.c"]

    def ex02(self):
        self.exercise_files = ["ft_strncat.c"]
        self.test_files = ["main.c"]