import logging
import os
import re
import shutil
import subprocess
from main import Colors, TestRunInfo
from testers.CommonTester import show_banner
from testers.ExecuteTripouille import ExecuteTripouille

logger = logging.getLogger()

AVAILABLE_TESTS = ['Tripouille']

FUNCTIONS_UNDER_TEST = [
    "isalpha",
    "isdigit",
    "isalnum",
    "isascii",
    "isprint",
    "strlen",
    "memset",
    "bzero",
    "memcpy",
    "memmove",
    "strlcpy",
    "strlcat",
    "toupper",
    "tolower",
    "strchr",
    "strrchr",
    "strncmp",
    "memchr",
    "memcmp",
    "strnstr",
    "atoi",
    "calloc",
    "strdup",
    "substr",
    "strjoin",
    "strtrim",
    "split",
    "itoa",
    "strmapi",
    "striteri",
    "putchar_fd",
    "putstr_fd",
    "putendl_fd",
    "putnbr_fd"
]

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

func_regex = re.compile(r"\w+\s+\*?ft_(\w+)\(.*")

class LibftTester():

    def __init__(self, info: TestRunInfo) -> None:
        if info.verbose:
            logger.setLevel("INFO")

        show_banner("libft")
        self.test_using(info, AVAILABLE_TESTS[0])

    def test_using(self, info: TestRunInfo, test):
        self.temp_dir = info.temp_dir
        self.tests_dir = os.path.join(info.tests_dir, test)
        self.source_dir = info.source_dir

        self.prepare_ex_files()
        norm_res = self.check_norminette()
        compile_res = self.create_library()

        if not compile_res:
            return "Project failed to create library"

        self.prepare_tests(test)

        if info.ex_to_execute:
            tx = ExecuteTripouille(info.temp_dir, [info.ex_to_execute])
            tx.prepare_tests()
            tx.execute(self.temp_dir, info.ex_to_execute)
        else:
            present = self.get_present()
            to_execute = intersection(present, FUNCTIONS_UNDER_TEST)

            tx = ExecuteTripouille(info.temp_dir, to_execute)
            tx.prepare_tests()
            tx.compile_test()
            tx.execute_test()

            missing = [f for f in FUNCTIONS_UNDER_TEST if f not in present]
            print(f"\n{Colors.LIGHT_RED}Missing functions: {Colors.NC}{' '.join(missing)}")

    def prepare_ex_files(self):
        if os.path.exists(self.temp_dir):
            logger.info(f"Removing already present directory {self.temp_dir}")
            shutil.rmtree(self.temp_dir)

        # os.makedirs(self.temp_dir)
        shutil.copytree(self.source_dir, self.temp_dir)

    def check_norminette(self):
        os.chdir(os.path.join(self.temp_dir))
        logger.info(f"On directory {os.getcwd()}")
        logger.info(f"Executing norminette")
        norm_exec = ["norminette", "-R", "CheckForbiddenSourceHeader"]

        result = subprocess.run(norm_exec, capture_output=True, text=True)

        print(
            f"{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(norm_exec)}{Colors.NC}:")
        if result.returncode != 0:
            print(f"{Colors.YELLOW}{result.stdout}{Colors.NC}")
        else:
            print(f"{Colors.GREEN}Norminette OK!{Colors.NC}")

        return result.returncode == 0

    def create_library(self):
        logger.info(f"On directory {os.getcwd()}")
        make_exec = ["make"]

        print(
            f"{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(make_exec)}{Colors.NC}:")
        subprocess.run(["make", "fclean"], capture_output=True, text=True)
        p = subprocess.run(make_exec, capture_output=True, text=True)

        if p.returncode == 0:
            print(f"{Colors.GREEN}make: OK!{Colors.NC}")
        else:
            print(f"{Colors.LIGHT_RED}Problem creating library{Colors.NC}")
            print(f"{Colors.YELLOW}{p.stdout}{Colors.NC}")
            print(f"{Colors.RED}{p.stderr}{Colors.NC}")

        return p.returncode == 0

    def prepare_tests(self, test):
        try:
            # delete destination folder if already present
            temp_dir = os.path.join(self.temp_dir, test)
            if os.path.exists(temp_dir):
                logger.info(f"Removing already present directory {temp_dir}")
                shutil.rmtree(temp_dir)

            # copy test framework
            logger.info(f"Copying {test} from {self.tests_dir} to {temp_dir}")
            shutil.copytree(self.tests_dir, temp_dir)

            # copy compiled library
            library = os.path.join(self.temp_dir, "libft.a")
            logger.info(
                f"Copying libft.a from {library} to {temp_dir}")
            shutil.copy(library, temp_dir)

            # copy header
            header = os.path.join(self.temp_dir, "libft.h")
            logger.info(
                f"Copying libft.h from {header} to {temp_dir}")
            shutil.copy(header, temp_dir)

            return True
        except Exception as ex:
            logger.info("Problem creating the files structure: ", ex)
            return False

    def get_present(self):
        header = os.path.join(self.temp_dir, "libft.h")
        with open(header, "r") as h:
            funcs_str = [line for line in h.readlines() if func_regex.match(line)]
            return [func_regex.match(line).group(1) for line in funcs_str]
