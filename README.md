# Francinette

A small and easy to use testing framework for the 42 projects.

Use `francinette` or `paco` inside a project folder to run it.


## Table of Contents
1. [Purpose](#purpose)
2. [Install](#install)
3. [Update](#update)
4. [Running](#Running)
5. [FAQ](#faq)
6. [Acknowledgments](#acknowledgments)

## Purpose:

This is designed to function as a kind of moulinette that you can execute in local.

That means that by executing `francinette` it will check `norminette`, compile the
code and execute the tests. This will give you more time to look at the code itself
when doing a review, instead of worrying about compiling the cloned code.

You can also use it as local tests, that you can check your own code against it.


## Install:
Francinette has an automatic installer.

Copy the line bellow to your console and execute it. It will automatically download the repo,
create the necessary folders and alias, and install a python virtual environment dedicated to
running this tool

```
sh -c "$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/install.sh)"
```

The francinette folder will be under your `$HOME` directory (`/User/<you_username>/`)

## Update:
Normally francinette will prompt you when there is a new version, and you can then update it.

If you disabled this functionality or need to update for other reasons run the command bellow:

```
sh -c "$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/update.sh)"
```

## Runnning:

If you are on a root of a project, francinette should be able to tell which project
it is and execute the corresponding tests.

```
/C00 $> francinette              # Execute the tests for C00

/C00/ex00 $> francinette         # Execute only the tests for ex00 in C00

/libft $> francinette            # Execute the tests for libft

~ $> francinette -h              # Shows the help message

libft $> francinette -t memset   # Execute only the test for memset

~ $> francinette git@repo42.com/intra-uuid-234
    # Clones the git present in `git@repo42.com/intra-uuid-234`
    # and executes the tests for the downloaded project
```

The name of the folder is not important. What is important is that you should have a `Makefile`
that contains the name of the project (for example `libft`). If there is no `Makefile`
`francinette` will not know what project to execute.

You can also use the shorter version of the command: `paco`

You can also use francinette to evaluate a project directly from a git repository link.

```
$> francinette git@repository.42.com/intra-uuid-391f552
                             v
                  git url to clone the project from
```

It should also know to which project is this repo and run the corresponding tests.

All the files are copied to the folder `~/francinette/temp/<project>`. In here is where the
norminette is checked, the code compiled and the tests executed. Normally you do not need to
access this directory for anything. But if you run into unexpected problems, this is where
the magic happens

## FAQ

If you have any questions I am probably in the barcelona cluster. Also, you can reach me on
slack under `fsoares-`

#### I'm more advanced than the tests you have available. When are you adding more tests?

When I reach that exercise. You can also add them yourself. But for that you need to also
create a `C0X_Tester.py` file. (Also there is a need to change the function `guess_project`
in `main.py` to recognize the files for that project)

#### This test that you put up is incorrect!

Well, you can change it yourself and create a pull request, or you can contact me indicating
for what exercise which test fails, and a description of what you think is wrong

## Acknowledgments

* To 42 for providing me this opportunity
* To [Tripouille](https://github.com/Tripouille) for their excellent (libftTester)[https://github.com/Tripouille/libftTester]