import os
import re
import logging
logger = logging.getLogger()


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    LIGHT_GREEN = '\033[1;32m'
    LIGHT_BLUE = '\033[1;36m'
    PURPLE = '\033[0;35m'
    LIGHT_PURPLE = '\033[1;35m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


    # Check norminette output

    # Copy prepared files (main.c, expected, etc)

    # Get the files that need to be compiled from the implementation

    # Compile and check for errors

    # Execute and compare with the expected values

def show_banner():
    message = f"Welcome to {Colors.PURPLE}Francinette{Colors.LIGHT_BLUE}, a 42 tester framework!"
    print(f"{Colors.LIGHT_BLUE}")
    print(f"╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                {message}                ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.NC}")


class CommonTester:

    def __init__(self, options):
        self.compile = None
        self.norm_ignore = None
        self.options = options
        logger.info(f"Options for this run {options}")
        self.available_tests = [test for test in dir(self) if re.match(r"ex\d{2}", test)]
        logger.info("tests to be run: %s", self.available_tests)

        show_banner()

        for test in self.available_tests:
            self.execute_test(test)

    def execute_test(self, test_to_execute):
        logger.info(f"starting execution of {test_to_execute}")
        ex_number = test_to_execute[-2:]
        if self.options["exercise"] and self.options["exercise"] != ex_number:
            # If a test is specified, then it only executes the matching test
            print(f"{Colors.YELLOW}--- Ex{ex_number} Ignored ---{Colors.NC}")
            return

        print(f"{Colors.LIGHT_GREEN}--- Testing Ex{ex_number} ---{Colors.NC}")
        test_fn = getattr(self, test_to_execute)()
        logger.info(f"files to compile with: {self.compile}")
        result = os.system("norminette " + " ".join(self.compile))
