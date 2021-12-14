from CommonTester import CommonTester


class C02_Tester(CommonTester):

    def ex00(self):
        self.compile = ["main.c", "ft_strcpy.c"]
        self.norm_ignore = ["main.c"]

    def ex01(self):
        self.compile = ["main.c", "ft_strncpy.c"]
        self.norm_ignore = ["main.c"]

    def ex02(self):
        self.compile = ["main.c", "ft_str_is_alpha.c"]
        self.norm_ignore = ["main.c"]

    def ex03(self):
        self.compile = ["main.c", "ft_str_is_numeric.c"]
        self.norm_ignore = ["main.c"]

    def ex04(self):
        self.compile = ["main.c", "ft_str_is_lowercase.c"]
        self.norm_ignore = ["main.c"]

