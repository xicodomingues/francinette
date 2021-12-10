# Francinette
A small and easy to use testing framework for the 42 C module

## Install:
Francinette has an automatic installer.

Copy the line bellow to your console and execute it. It will automatically download the repo, create the necessary folders and alias, and install a python virtual environment dedicated to running this tool

```
sh -c "$(curl -fsSL https://raw.github.com/francinette/install.sh)"
```

The francinette folder will be under your `$HOME` directory (`/User/<you_username>/`)


## Runnning:
If you have the following folder structure inside francinette you just need to write francinette inside the project / exercise that you wish to run, and it will automatically run.

### Folder Structure:
```
francinette
├── c00                      # This is the repository where you will deliver the files.
│   │                        # The project names need to folow cXX convention.
│   ├── ex00                 # same for exercises
│   │   └── ft_putchar.c
│   ├── ex01
│   │   └── ft_print_alphabet.c
│   └── ex02
│       └── ft_print_reverse_alphabet.c
├── c01 
│   └── ex00     
│
├── files                    # This is the directory where the main.c and expected files
│   │                        # should be located For them to be used without configuration
│   └── c00
│       ├── ex00
│       │   └── main.c
│       ├── ex01
│       │   ├── expected
│       │   └── main.c
│       ├── ex02
│       │   └── main.c
│       └── ex03
│           ├── expected
│           └── main.c 
│
├── temp                     # Where the magic happens. In where it will copy the files
│   └── c00                  # from your exercises dir, from the files dir, executes
│       ├── ex00             # the norminette, compiles, executes the C program and if
│       │   ├── a.out        # if there is an expected file, it will compare the output
│       │   ├── ft_putchar.c
│       │   └── main.c
│       └── ex01
│           ├── a.out
│           ├── expected
│           ├── ft_print_alphabet.c
│           ├── main.c
│           └── out
│
├── C00_Tester.py          # Each project needs to have a corresponding tester
├── CommonTester.py        # Contains the common parts to all the testers (comile, norm, etc)
├── LICENSE
├── README.md              # This document
├── install.sh             # The script to install francinette
├── main.py                # The point of entry for the francinette
├── requirements.txt       # python things
├── tester.sh              # The script that will execute the tests
└── venv                   # The python virtual environment, not really relevant
```

I would recommend using this structure, because it automates many of the configurations. But you can specify your own folders. Explained in the `Configuration` part of ths document


```


## Configuration