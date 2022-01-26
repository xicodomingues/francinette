from utils.TerminalColors import TC


def show_banner(project):
	message = f"Welcome to {TC.B_PURPLE}Francinette{TC.B_BLUE}, a 42 tester framework!"
	submessage = f"{project}"
	project_message = f"{TC.B_YELLOW}{project}{TC.B_BLUE}"
	size = 30 - len(submessage)
	project_message = " " * (size - (size // 2)) + project_message + " " * (size // 2)
	print(f"{TC.B_BLUE}╔══════════════════════════════════════════════════════════════════════════════╗")
	print(f"{TC.B_BLUE}║                {message}                ║")
	print(f"{TC.B_BLUE}╚═══════════════════════╦══════════════════════════════╦═══════════════════════╝")
	print(f"{TC.B_BLUE}                        ║{project_message}║")
	print(f"{TC.B_BLUE}                        ╚══════════════════════════════╝{TC.NC}")
