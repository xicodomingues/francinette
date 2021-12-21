# Francinette
A small and easy to use testing framework for the 42 C module.

It is designed to automate checking `norminette`, compiling the code and executing the tests, to give you more time to look at the code itself.

## Install:
Francinette has an automatic installer.

Copy the line bellow to your console and execute it. It will automatically download the repo,
create the necessary folders and alias, and install a python virtual environment dedicated to running this tool

```
sh -c "$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/install.sh)"
```

The francinette folder will be under your `$HOME` directory (`/User/<you_username>/`)

## Update:
To update francinette run the command bellow

```
sh -c "$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/update.sh)"
```

## Runnning:

If you are on a root of a project and under it you have the exercises, francinette should be
able to tell which project it is and execute the corresponding tests.

```
in: /C00 $> francinette
```

you can also use the shorter version of the command: `paco`

In the case above, francinette should run the tests in C00.

You can also use francinette to evaluate a project from github.

```
$> francinette git@repository.42.com/intra-uuid-8e9b82a1-59b4-43cd-ah34-639a79beeb5f-391f552
                             v
                  git url to clone the project from
```

It should also know to which project is this repo and run the corresponding tests

## Configuration / Usage

```
$> francinette -h
```
This shows the help message.

```
in: francinette/c00 $> francinette
```

This will execute the tests for the project c00

```
in: francinette/c00/ex00 $> francinette
```

This will execute the test only for ex00 of the project c00


```
in: francinette/c00 $> francinette -e ex01
```

This will execute the test only for ex01 of the project c00

```
$> francinette <a git repo with the c00 solved exercises>
```

It clones the git, and executes the tests in `francinette/mains` against the clonned code.


### Folder Structure:
```
francinette
│
├── files                    # This is the directory where the main.c and expected files are
│   │                        # You can change the mains or the expected files to improve the tests
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
├── C01_Tester.py
├── C02_Tester.py
├── C03_Tester.py
├── CommonTester.py        # Contains the common parts to all the testers (comile, norm, etc)
├── LICENSE
├── README.md              # This document
├── install.sh             # The script to install francinette
├── main.py                # The point of entry for the francinette
├── requirements.txt       # python things
├── tester.sh              # The script that will execute the tests
└── venv                   # The python virtual environment, not really relevant
```


## FAQ

If you have any questions you know where to find me. Also, on slack under 'fsoares-'

#### I'm more advanced than the tests you have available. When are you adding more tests?

When I reach that exercise. You can also add them yourself. But for that you need to also
create a `C0X_Tester.py` file. (Also there is a need to change the function `guess_project`
in `main.py` to recognize the files for that project)

#### This test that you put up is incorrect!

Well, you can change it yourself and create a pull request, or you can contact me so we can
change it together and be friends 😜