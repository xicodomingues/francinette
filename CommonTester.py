from dataclasses import dataclass
import os
import re
import logging
import shutil
import subprocess

from main import TestRunInfo
from main import Colors
from pathlib import Path

logger = logging.getLogger()


DEFAULT_COMPILE_FLAGS = ["-Wall", "-Wextra", "-Werror"]
IGNORED_EXERCISE_HEADER = f"{Colors.YELLOW}" \
        "═════════════════════════════════ #### Ignored ═════════════════════════════════" \
        f"{Colors.NC}"

EXERCISE_HEADER= f"{Colors.LIGHT_BLUE}" \
        "═════════════════════════════════ Testing #### ═════════════════════════════════" \
        f"{Colors.NC}"

TEST_PASSED = f"\n{Colors.LIGHT_GREEN}" \
        "══════════════════════════════    #### passed!    ══════════════════════════════" \
        f"{Colors.NC}"

TEST_FAILED = f"\n{Colors.LIGHT_RED}" \
        "══════════════════════════════    #### failed!    ══════════════════════════════" \
        f"{Colors.NC}"

TEST_NOT_PRESENT = f"\n{Colors.YELLOW}" \
        "══════════════════════════════  #### not present  ══════════════════════════════" \
        f"{Colors.NC}"


def show_banner(project):
    message = f"Welcome to {Colors.LIGHT_PURPLE}Francinette{Colors.LIGHT_BLUE}, a 42 tester framework!"
    project_message = f"{Colors.LIGHT_YELLOW}Executing {project.upper()}{Colors.LIGHT_BLUE}"
    print(f"{Colors.LIGHT_BLUE}")
    print(f"╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                {message}                ║")
    print(f"╚═══════════════════════╦══════════════════════════════╦═══════════════════════╝")
    print(f"                        ║         {project_message}        ║")
    print(f"                        ╚══════════════════════════════╝")
    print(f"{Colors.NC}")


@dataclass
class VeriOut:
    returncode: int
    stdout: str


class CommonTester:

    def __init__(self, info: TestRunInfo):
        self.compile_flags = []
        self.exercise_files = []
        self.test_files = []
        self.temp_dir = info.temp_dir
        self.source_dir = info.source_dir
        self.tests_dir = info.tests_dir
        self.project = info.project
        self.selected_test = info.ex_to_execute

        if info.verbose:
            logger.setLevel(logging.INFO)

        if self.selected_test:
            test = "ex" + self.selected_test[-2:]
            test_ok = self.execute_test(test)
            self.show_result(self.selected_test, test_ok)
            return

        self.available_tests = [test for test in dir(self) if re.match(r"^ex\d{2}$", test)]
        logger.info("tests found: %s", self.available_tests)

        show_banner(info.project)

        test_status = {}
        for test in self.available_tests:
            test_ok = self.execute_test(test)
            test_status[test] = test_ok
            self.show_result(test, test_ok)

            print("\n")
            self.clean_up(test)

        self.print_summary(test_status)

    def show_result(self, test, test_ok):
        if test_ok == True:
            print(TEST_PASSED.replace("####", test.title()))
        elif test_ok == False:
            print(TEST_FAILED.replace("####", test.title()))
        elif test_ok == "Test Not Present":
            print(TEST_NOT_PRESENT.replace("####", test.title()))

    def print_summary(self, test_status):
        ok_tests = [test for test, st in test_status.items() if st is True]

        print(f"{Colors.LIGHT_GREEN}Passed tests: {' '.join(ok_tests)}{Colors.NC}")
        failed_tests = [test for test, st in test_status.items() if st is False]
        if failed_tests:
            print(f"{Colors.LIGHT_RED}Failed tests: {' '.join(failed_tests)}{Colors.NC}")


    def pass_norminette(self, test):
        os.chdir(os.path.join(self.temp_dir, test))
        logger.info(f"On directory { os.getcwd() }")
        logger.info(f"Executing norminette on files: {self.exercise_files}")
        norm_exec = ["norminette", "-R", "CheckForbiddenSourceHeader"] + self.exercise_files

        result = subprocess.run(norm_exec, capture_output=True, text=True)

        print(f"{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(norm_exec)}{Colors.NC}:")
        if result.returncode == 0:
            print(f"{Colors.GREEN}{result.stdout}{Colors.NC}")
        else:
            print(f"{Colors.YELLOW}{result.stdout}{Colors.NC}")

        return result.returncode == 0


    def compile_files(self):
        files = self.test_files + self.exercise_files
        flags = self.compile_flags if self.compile_flags else DEFAULT_COMPILE_FLAGS

        logger.info(f"compiling files: {files} with flags: {flags}")
        #result = os.system(f"gcc { " ".join(flags) } { " ".join(files) }")
        gcc_exec = ["gcc"] + flags + files

        print(f"{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(gcc_exec)}{Colors.NC}:")
        p = subprocess.Popen(gcc_exec);
        p.wait()

        if p.returncode == 0:
            print(f"{Colors.GREEN}gcc: OK!{Colors.NC}")
        else:
            print(f"{Colors.LIGHT_RED}Problem compiling files{Colors.NC}")

        return p.returncode


    def execute_program(self, test):
        logger.info(f"Running the output of the compilation: ")
        logger.info(f"On directory { os.getcwd() }")

        print(f"\n{Colors.CYAN}Executing: {Colors.WHITE}./a.out | cat -e{Colors.NC}:")

        ps = subprocess.Popen(('./a.out'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = subprocess.check_output(('cat', '-e'), stdin=ps.stdout)
        ps.wait()
        output = output.decode('ascii', errors="replace")

        if ps.returncode == 0:
            logger.info("Executed program successfully main")
            print(output)
        else:
            print(f"{Colors.RED}{output}{Colors.NC}")
            print(f"{Colors.LIGHT_RED}Error Executing the program! (Most likely SegFault){Colors.NC}")
            location = os.path.join(self.temp_dir, test)
            print(f"The {Colors.WHITE}main.c{Colors.NC} and {Colors.WHITE}a.out{Colors.NC} used in this "
                    f"test are located at:\n{Colors.WHITE}{location}{Colors.NC}")

        return output


    def do_diff(self):
        diff_exec = ["diff", "--text", "expected", "out"]
        print(f"\n{Colors.CYAN}Executing: {Colors.WHITE}{' '.join(diff_exec)}{Colors.NC}:")

        result = subprocess.run(diff_exec, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}diff: No differences{Colors.NC}")
        else:
            print(f"{Colors.LIGHT_PURPLE}< expected, > your result{Colors.NC}")
            print(f"{Colors.RED}{result.stdout}{Colors.NC}")

        return result.returncode == 0


    def do_verification_fn(self, verification_fn):
        print(f"\n{Colors.CYAN}Executing function: {Colors.WHITE}{verification_fn.__name__}{Colors.NC}:")

        result = verification_fn()
        if result.returncode == 0:
            print(f"{Colors.GREEN}Everything OK!{Colors.NC}")
        else:
            print(f"{Colors.RED}{result.stdout}{Colors.NC}")

        return result.returncode == 0


    def compare_with_expected(self, output, test):
        expected_file = os.path.join(os.getcwd(), 'expected')

        if not os.path.exists(expected_file):
            return True

        out_file_path = os.path.join(os.getcwd(), 'out')

        logger.info(f"Creating out file: {out_file_path} with content {output}")
        with open(out_file_path, 'w') as out_file:
            out_file.write(output)
            out_file.close();

            verification_fn = getattr(self, f"{test}_verification", None)
            if verification_fn:
                return self.do_verification_fn(verification_fn)
            else:
                return self.do_diff()


    def execute_test(self, test_to_execute):
        logger.info(f"starting execution of {test_to_execute}")

        print(EXERCISE_HEADER.replace("####", test_to_execute))
        print()
        getattr(self, test_to_execute)()

        logger.info("Preparing the test")
        ready = self.prepare_test(test_to_execute)
        if not ready:
            return "Test Not Present"

        norm_passed = self.pass_norminette(test_to_execute)
        status = self.compile_files()
        if status != 0:
            return False

        output = self.execute_program(test_to_execute)
        return self.compare_with_expected(output, test_to_execute) and norm_passed


    def prepare_test(self, test):
        try:
            # delete destination folder if already present
            temp_dir = os.path.join(self.temp_dir, test)
            if os.path.exists(temp_dir):
                logger.info(f"Removing already present directory {temp_dir}")
                shutil.rmtree(temp_dir)

            os.makedirs(temp_dir)

            # copy exercise files from source folder
            for filename in self.exercise_files:
                source_path = os.path.join(self.source_dir, test, filename)
                dest_path = os.path.join(temp_dir, filename)
                logger.info(f"Copying source file: {source_path} to {dest_path}")
                shutil.copy(source_path, dest_path)

            # copy files from test folder and the expected files
            for filename in self.test_files:
                source_path = os.path.join(self.tests_dir, test, filename)
                dest_path = os.path.join(temp_dir, filename)
                logger.info(f"Copying test file: {source_path} to {dest_path}")
                shutil.copy(source_path, dest_path)

            expected_path = os.path.join(self.tests_dir, test, "expected")
            if os.path.exists(expected_path):
                logger.info(f"Copying expected file: {source_path} to {dest_path}")
                shutil.copy(expected_path, temp_dir)

            # remove a.out
            program_path = os.path.join(self.tests_dir, test, "a.out")
            if os.path.exists(program_path):
                logger.info(f"Removing file: {program_path}")
                shutil.rmtree(program_path)

            # remove out
            program_path = os.path.join(self.tests_dir, test, "out")
            if os.path.exists(program_path):
                logger.info(f"Removing file: {program_path}")
                shutil.rmtree(program_path)

            return True
        except Exception as ex:
            logger.info("Problem creating the files structure: ", ex)
            return False


    def clean_up(self, test):
        self.compile_flags = []
        self.compile = []
        self.norm_ignore = []
