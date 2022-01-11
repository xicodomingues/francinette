import logging
import os
import re
import subprocess
import shutil
import sys
from main import Colors, TestRunInfo
from testers.CommonTester import DEFAULT_COMPILE_FLAGS, show_banner

logger = logging.getLogger()

def create_main(funcs):
    with open('main.cpp', 'w') as f:
        for func in funcs:
            f.write(f"int main_{func}(void);\n")

        f.write("\nint iTest = 1;\n")
        f.write("int main(void) {\n")
        for func in funcs:
            f.write(f"    iTest = 1;\n")
            f.write(f"    main_{func}();\n")
        f.write("}\n")


class ExecuteTripouille:

    def __init__(self, temp_dir, to_execute) -> None:
        self.temp_dir = temp_dir
        self.to_execute = to_execute
        self.folder = "Tripouille"
        self.git_url = "https://github.com/Tripouille/libftTester"

    def prepare_tests(self):
        os.chdir(os.path.join(self.temp_dir, self.folder, 'tests'))

        logger.info("Rewriting the mains to create a super main.cpp")
        for file in os.listdir("."):
            with open(file, "r") as f:
                fname = file.replace('ft_', '').replace('_test.cpp', '')
                content = f.read()  \
                    .replace("main(void)", f"main_{fname}(void)")  \
                    .replace("int iTest = 1;", 'extern int iTest;')

            logger.info(f"Saving file {file}")
            with open(file, "w") as f2:
                f2.write(content)

        logger.info("Creating the super main!")
        create_main(self.to_execute)

    def compile_test(self):
        os.chdir(os.path.join(self.temp_dir, self.folder))
        logger.info(f"On directory {os.getcwd()}")
        print(f"\n{Colors.CYAN}Compiling tests from: {Colors.WHITE}{self.folder}{Colors.NC} ({self.git_url}):")

        # -g3 (for debug???)
        command = (f"clang++ -g3 -ldl -std=c++11 -I utils/ -I . utils/sigsegv.cpp utils/color.cpp " +
                   f"utils/check.cpp utils/leaks.cpp tests/main.cpp -o main.out").split(" ")

        for file in self.to_execute:
            command.append(f"tests/ft_{file}_test.cpp")

        command += ["-L.", "-lft"]
        print(" ".join(command))
        p = subprocess.Popen(command)
        p.wait()
        return p

    def execute_test(self):
        if sys.platform.startswith("linux"):
            execute = f"valgrind -q --leak-check=full ./main.out".split(" ")
        else:
            execute = ["./main.out"]

        print(f"\n{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(execute)}{Colors.NC}:")

        p = subprocess.run(execute, capture_output=True, text=True)
        print(p.stdout)

        res = [(int(m.group(1)), m.group(2))
               for m in re.finditer("(\d+)\.(\w+)", p.stdout)]
        for r in res:
            color = Colors.GREEN if r[1] == 'OK' else Colors.RED
            #print(f"{color}{r[0]}.{r[1]} ", end="")
        print(Colors.NC)
        return res

