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
If you have the following folder structure inside francinette you just need to write `francinette` inside the project / exercise that you wish to run, and it will automatically run.

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
│   │                        # should be located for them to be used without configuration
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
│   └── c00                  # from your exercises dir, from the files dir, execute the
│       ├── ex00             # norminette, compile, execute the C program and if there
│       │   ├── a.out        # is an expected file, it will compare the output from the
│       │   ├── ft_putchar.c # main.c and this expected file
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

I would recommend using this structure, because it automates many of the configurations. But you can specify your own folders. Explained in the `Configuration` part of this document


## Configuration / Usage

If you have the folder structure as indicated above you just need to navigate to the desired
project folder, like for example `~/francinette/c00` and execute the `francinette` command.


In case you are using this directory structure, you can tweak the functionality with the following parameters:

```
$> francinette -h

This shows the help message.


francinette/c00 $> francinette

This will execute the tests for the project c00


$> francinette c00

This will execute the tests for the project c00 no matter wich direcotry I'm in


$> francinette --base ~/my/custom/temp/dir
or
$> francinette -b ~/my/custom/temp/dir


francinette will use this as the directory where it will put the temp files. The temp files are the files used for execution of the tests. By default this is in ~/francinette/temp/


$> francinette --files ~/where/the/main.c/and/expected files are.

francinette will get the main.c's and the expected files from this directory instead of the default one. The default one is located in ~/francinette/files/
```