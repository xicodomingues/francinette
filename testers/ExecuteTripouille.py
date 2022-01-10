import logging
import os
import re
import subprocess
from main import Colors, TestRunInfo
from testers.CommonTester import DEFAULT_COMPILE_FLAGS, show_banner


class ExecuteTripouille:

    def __init__(self, temp_dir) -> None:
        self.temp_dir = temp_dir

    def execute(self, test, to_execute):
        out = self.compile_test(test, to_execute)
        if (out.returncode != 0):
            print(f"{Colors.RED}Problem compiling test.")
            return f"Problem compiling test for {to_execute}"

        self.check_output(self.execute_tests())

    def compile_test(self, test, to_execute):
        os.chdir(os.path.join(self.temp_dir, test))
        print(f"{to_execute} ", end="", flush=True)

        # TODO: improve compilation
        command = (f"clang++ -g3 -ldl -std=c++11 -I . -I utils/ utils/sigsegv.cpp utils/color.cpp "
                   f"utils/check.cpp utils/leaks.cpp tests/ft_{to_execute}_test.cpp -L . -lft "
                   f"-o {to_execute}.out".split(" "))
        p = subprocess.run(command, capture_output=True, text=True)
        return p

    def execute_test(self, to_execute):
        print(f"{to_execute.ljust(20)}: ", end="", flush=True)
        execute = [f"./{to_execute}.out"]
        p = subprocess.run(execute, capture_output=True, text=True)

        res = [(int(m.group(1)), m.group(2))
               for m in re.finditer("(\d+)\.(\w+)", p.stdout)]
        for r in res:
            color = Colors.GREEN if r[1] == 'OK' else Colors.RED
            print(f"{color}{r[0]}.{r[1]} ", end="")
        print(Colors.NC)
        return res

