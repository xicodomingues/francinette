from CommonTester import CommonTester


class C01_Tester(CommonTester):


    def ex00(self):
        self.compile = ["main.c", "ft_ft.c"]
        self.norm_ignore = ["main.c"]

    def ex01(self):
        self.compile = ["main.c", "ft_ultimate_ft.c"]
        self.norm_ignore = ["main.c"]

    def ex02(self):
        self.compile = ["main.c", "ft_swap.c"]
        self.norm_ignore = ["main.c"]

    def ex03(self):
        self.compile = ["main.c", "ft_div_mod.c"]
        self.norm_ignore = ["main.c"]

    def ex04(self):
        self.compile = ["main.c", "ft_ultimate_div_mod.c"]
        self.norm_ignore = ["main.c"]

    def ex05(self):
        self.compile = ["main.c", "ft_putstr.c"]
        self.norm_ignore = ["main.c"]

    def ex06(self):
        self.compile = ["main.c", "ft_strlen.c"]
        self.norm_ignore = ["main.c"]

    def ex07(self):
        self.compile = ["main.c", "ft_rev_int_tab.c"]
        self.norm_ignore = ["main.c"]

    def ex08(self):
        self.compile = ["main.c", "ft_sort_int_tab.c"]
        self.norm_ignore = ["main.c"]
