# makefiling

`makefiling` is a collection of hands-on exercises for GNU Make, covering section by section
All contents of [makefiletutorial.com](https://makefiletutorial.com/).

Each exercise is a directory that can be run independently, with a `Makefile` and a
`checks.json`. The initial `Makefile` intentionally had missing rules, miswritten variables, or
Broken dependency; you need to modify it so that `./makefiling run` will pass.

It is recommended to start with the [Basic Route](docs/basics.md) for your first study: it strings the first 20 questions into one
The main line of "predict → modify → observe → explain", then use [small project](docs/first-project.md)
Connect concepts.

## Practice Topics

A total of **13 topics and 177 exercises**, covering the main operational content of the tutorial; Getting Started
Links to reading about alternative tools and Make implementation background are also provided.

| Topics | Number of exercises | Corresponding tutorial sections | Table of Contents |
| --- | ---: | --- | --- |
| Getting Started | 6 | Why do Makefiles exist?, Running the Examples (including background reading) | [`00_getting_started`](exercises/00_getting_started/) |
| Makefile Syntax and the Essence of Make | 11 | Makefile Syntax, The essence of Make | [`01_syntax_and_essence`](exercises/01_syntax_and_essence/) |
| More Quick Examples | 10 | More quick examples, Make clean | [`02_quick_examples`](exercises/02_quick_examples/) |
| Variables | 14 | Variables, Automatic Variables | [`03_variables`](exercises/03_variables/) |
| Targets | 12 | Targets, The all target, Multiple targets | [`04_targets`](exercises/04_targets/) |
| Automatic Variables and Wildcards | 13 | * Wildcard, % Wildcard, Automatic Variables | [`05_wildcards_and_automatic_variables`](exercises/05_wildcards_and_automatic_variables/) |
| Fancy Rules | 16 | Implicit Rules, Static Pattern Rules, Static Pattern Rules and Filter, Pattern Rules, Double-Colon Rules | [`06_fancy_rules`](exercises/06_fancy_rules/) |
| Commands and Execution | 22 | Command Echoing/Silencing, Command Execution, Default Shell, Double dollar sign, Error handling with -k, -i, and -, Interrupting or killing make, Recursive use of make, Export, environments, and recursive make, Arguments to make | [`07_commands_and_execution`](exercises/07_commands_and_execution/) |
| Variables Pt. 2 | 16 | Flavors and modification, Command line arguments and override, List of commands and define, Target-specific variables, Pattern-specific variables | [`08_variables_pt2`](exercises/08_variables_pt2/) |
| Conditional Part of Makefiles | 14 | Conditional if/else、Check if a variable is empty、Check if a variable is defined、$(MAKEFLAGS) | [`09_conditionals`](exercises/09_conditionals/) |
| Functions | 20 | First Functions, String Substitution, The foreach function, The if function, The call function, The shell function, The filter function | [`10_functions`](exercises/10_functions/) |
| Other Features | 14 | Include Makefiles, The vpath Directive, Multiline, .phony, .delete_on_error | [`11_other_features`](exercises/11_other_features/) |
| Makefile Cookbook | 9 | Makefile Cookbook | [`12_cookbook`](exercises/12_cookbook/) |

The `README.md` of each topic will list the list and sequence of exercises for that topic; see [docs/curriculum.md](docs/curriculum.md) for a topic-by-topic comparison table.

## Features

- **Complete coverage tutorial**: from the first rule, variables, wildcards, to pattern rules, conditions,
  Functions and the cookbook at the end, each section of the tutorial has corresponding exercises.
- **Contract-driven**: The acceptance conditions of each exercise are written in `checks.json` - which commands to run,
  The expected exit code, standard output, and what files should be on disk after the command ends. runner
  Just an interpreter of this contract.
- **Isolated Run**: Exercises will be copied to `build/makefiling/` and then executed, so `make`
  The generated `.o`, executables and intermediate files do not pollute `exercises/`,
  No additional pollution to git; `git status` will only reflect your edits to the exercise file itself.
- **Comes with CLI**: list, run, prompt, view answers, reset progress and listen for file changes.
- **Suitable for beginners**: `./makefiling start` provides a basic route of 20 questions, with prompts expanded by level.
  Preserves the working directory on failure and displays make's original diagnostics.
- **Almost zero dependencies**: only requires `make` and Python 3 (read `cat`, `touch`,
  Standard Unix tools such as `grep`; additional `cc` is required for exercises involving compilation).
- **Answers are separated from initial templates**: `solutions/` Save reference answers, `templates/`
  Save the original exercise, `exercises/` is the directory where you actually modified it.
- **Tutorial Comparison**: Each exercise is marked with its corresponding tutorial section, which can be read against the original text.
- **Modern Engineering Structure**: Makefile, CMake Presets, CTest, CI, Docker,
  EditorConfig.

## Quick start

### Environmental requirements

- GNU Make 3.81+ or 4.x
-Python 3.8+
- `cc` (required only for exercises involving compiling C; either GCC or Clang will do)

On Linux you usually only need:

```sh
sudo apt install build-essential python3
```

### Run

```sh
# View all exercises
./makefiling list

# Start basic route
./makefiling start
./makefiling list --basic

# Run the next unfinished exercise
./makefiling run

#Run the specified exercise (supports full ID, directory name or unique suffix)
./makefiling run 08_variables_pt2/01_recursive_vs_simply_expanded
./makefiling run 01_first_rule

# View tips
./makefiling hint 01_first_rule --level 1

# See what is being checked for this exercise
./makefiling hint 01_first_rule --steps

# View reference answers
./makefiling solution 01_first_rule

#Apply answers directly (will overwrite your exercise file)
./makefiling solution 01_first_rule --apply

# Resume initial practice
./makefiling reset 01_first_rule

# Monitor file changes and automatically rerun after saving
./makefiling watch 01_first_rule
```

You can also use Makefile:

```sh
make list
make run
make verify
make selftest
make test
make doctor
make clean
```

## Learning process

1. Read the goals and tips at the top of `exercises/<topic>/README.md` and `Makefile`.
2. Modify `exercises/<topic>/<slug>/Makefile` (if necessary, also modify the
   auxiliary files), run `./makefiling run <exercise>`.
3. If you get stuck, first use `./makefiling hint <exercise> --level 1`, and then read the instructions of make carefully.
   stderr; gradually increase to `--level 3` when necessary. On failure the runner prints the work it retained
   Directory and retry commands that can be directly copied can be entered and reproduced manually.
4. Continue to the next exercise after passing; progress is recorded in `.makefiling/progress.json`.
5. After completing a topic, check whether you understand the relevant concepts by referring to `docs/knowledge-map.md`.
6. Finally run `./makefiling verify` to verify all reference answers; `./makefiling selftest`
   What is checked is the original template and reference answer in the warehouse, and it will not fail because you have already completed a certain question.

Some exercises will **directly fail** at the beginning, some can run but the output is wrong, and some will report
`missing separator` - this is intentional: the Makefile's tab rules are tutorials themselves
Lesson one.

## Project structure

```text
.
├── makefiling # Zero dependency Python CLI
├── exercises/ # the exercises you want to modify
│ ├── 00_getting_started/
│ │ ├── README.md
│ │ └── 01_first_rule/
│ │ ├── Makefile # Practice ontology
│ │ └── checks.json # Acceptance contract
│ └── ...
├── solutions/ # Reference answers (same structure as exercises)
├── templates/ # Original exercise for ./makefiling reset
├── tools/
│ ├── generate_exercises.py # Generator
│ ├── spec.py # Specification data structure and checking steps DSL
│ └── specs_*.py # One specification file for each topic
├── docs/
│ ├── basics.md # 20-question basic route for beginners
│ ├── first-project.md # Use cookbook to complete a small project
│ ├── architecture.md # Generator, runner, contract design
│ ├── curriculum.md # List all exercises by tutorial section
│ └── knowledge-map.md # List coverage by GNU Make knowledge area
├── CMakeLists.txt
├── CMakePresets.json
├── Makefile
└── Dockerfile
```

## Build method

### Method 1: CLI + run on demand (recommended)

`./makefiling` only relies on the Python standard library. It copies exercises to
A separate temporary directory in `build/makefiling/` and execute the commands in the contract. This method is suitable for daily learning,
Also allows multiple check commands to be run simultaneously.

```sh
./makefiling doctor
./makefiling verify
```

### Method 2: Makefile

```sh
make verify
make selftest
make check-generated
```

### Method 3: CMake + CTest

Each reference answer is registered as a CTest test:

```sh
cmake --preset default
ctest --preset default
```

This project has no products that need to be compiled, so `cmake --build` is empty; CTest test
Call `./makefiling verify <exercise>` directly.

### Method 4: Docker

```sh
docker build -t makefiling .
docker run --rm -it -v "$PWD:/makefiling" makefiling ./makefiling list
```

## About make version

The tutorial is based on **GNU Make**, which is the standard implementation on Linux and macOS. of this project
The exercises can be passed on both GNU Make 3 and 4. CI uses the version that comes with Ubuntu.

The syntax of BSD make and nmake is different from this tutorial, and the exercises in this project do not apply to them.

## Add new exercise

Exercises are generated from specifications in `tools/specs_*.py`. Each specification contains the correct `Makefile`,
A set of checking steps, and a set of "correct fragment → initial fragment" replacements. Such exercises and answers
Will not be out of sync.

```sh
# Edit tools/specs_*.py
python3 tools/generate_exercises.py
./makefiling verify
./makefiling selftest
python3 tools/generate_exercises.py --check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and
[docs/architecture.md](docs/architecture.md).

## License

The project code uses the MIT License, see [LICENSE](LICENSE).

## Reference

- [makefiletutorial.com](https://makefiletutorial.com/) —— The source of the topic for this project
- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [rustlings](https://github.com/rust-lang/rustlings) - the formal source of the exercise set