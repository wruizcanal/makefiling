#Contributing

Thanks for your willingness to improve `makefiling`. The core principles of this project are:

1. The exercise must be able to run independently using the `make` that comes with the system and does not rely on third-party tools.
2. The initial state must fail; the reference answer must pass.
3. Each exercise only focuses on one concept, but the relevant details can be explained thoroughly.
4. Prompts should guide thinking rather than give direct answers.
5. Each exercise is labeled with its corresponding makefiletutorial.com section.
6. The exercises and reference answers are synchronized by the generator. Do not manually edit the generated files.

## Add an exercise

1. Find the corresponding topic specification file `tools/specs_<topic>.py`, if not, create a new one
   (The file name must be consistent with the topic name).
2. Call `ex(...)` to add specifications:

```python
ex(
    topic="03_variables",
    slug="13_new_exercise",
    title="...",
    objective="...",
    reference="Variables", # Tutorial section name
    hint="...",
    makefile="""
target:prereq
\tcommand
""",
    steps=[
        mk(stdout="what make prints", stdout_mode="contains"),
        mk("other-target", exit_code=2, stderr="No rule to make target"),
    ],
    breaks=[("correct text", "learner text")],
),
```

3. Regenerate and verify:

```sh
python3 tools/generate_exercises.py
./makefiling verify
./makefiling selftest
python3 tools/generate_exercises.py --check
make check-tracked
```

`make check-tracked` confirms that each file under `exercises/`, `solutions/`, `templates/`
Really entered the warehouse. The exercise will intentionally carry files such as `report.d` and `blah.o` that look like build products.
Once broad `*.d` / `*.o` rules appear in `.gitignore`, they will only exist locally and not
Exists in clone - local is all green, CI is all red. CI will also run this step.

## How to write specifications

### Tab

The recipe line must start with a real TAB. The specifications are Python source code, which is not visible if you write TAB directly.
It is easy to lose, so it is agreed to use `\t` to escape:

```python
makefile="""
hello:
\techo "Hello, World"
""",
```

Python will turn it into a real TAB. Literal backslashes required in the Makefile are written as `\\`.

### breaks

`breaks` is a list of `(correct fragments, initial fragments)`, which the generator applies in turn to the correct
In terms of content, get the initial version that learners see. There must be at least one substitution, and the substitution must be
Make at least one check step fail - `./makefiling selftest` will force a check for this.

Use `file_breaks` when you want to change auxiliary files (such as Makefile and C source code in subdirectories):

```python
file_breaks=[("sub/Makefile", "Correct Break", "Initial Break")],
```

### Check steps

Each step is `mk(...)` (run make) or `step(cmd, ...)` (run any command),
You can specify:

| Parameters | Meaning |
| --- | --- |
| `exit_code` | Desired exit code, default 0 |
| `stdout` / `stdout_mode` | Expectations and comparisons for standard output |
| `stderr` / `stderr_mode` | Expectations and comparisons for standard error |
| `env` | Additional environment variables |
| `files` | Files that must exist after this step and have exactly the same content |
| `missing` | Files that must not exist after this step |
| `description` | The name of this step as it appears in the report |

For comparison methods, see [docs/architecture.md](docs/architecture.md#matching pattern). The default is
`contains_lines`; use `contains` and `ordered_lines` first, only when
Use `exact` only when necessary.

### The expected value must be real

Before writing expectations, create a temporary directory under `/tmp` and put the correct content and auxiliary files into it.
Run the command you plan to put into `steps` and copy the observed output. Don't rely on
Remember to guess what make will print - this sentence is a hard requirement in this project.

### Certainty

- Do not use changing inputs such as `date`, `$$RANDOM`, `$$PPID` and the like.
- Do not use absolute paths; the working directory will be normalized to `<stage>`.
- No `sleep`, no dependence on timing.
- No access to the Internet.
- Only operate files in the arrangement directory.

### Timestamp must be specified explicitly

The runner will uniformly change the staging files to a fixed time long ago (see
[docs/architecture.md](docs/architecture.md)), so "the document just written out by the recipe is better than the exercise
The built-in file "New" is automatically established, so you don't need to worry about it.

But **don't use naked `touch` to create "a certain file has been updated"**. The previous recipe just wrote out the target
Come, and some file systems (CI runner is) quantify the timestamp to the whole second, `touch` and the target may fall
During the same tick, make will think there is nothing to do and the assertion will fail randomly. To specify two times explicitly:

```python
step("touch", "-t", "202001010000", "out.txt",
     description="age the built file"),
step("touch", "-t", "202101010000", "b.txt",
     description="make the second prerequisite newer"),
```

First adjust the target to the old one, and then adjust the files that need to be updated to a later date. There is a one-year difference between the two, and it will work at any time stamp granularity.
Not vague. The format of `touch -t` is `[[CC]YY]MMDDhhmm`; the time must fall in the past, otherwise make
Clock skew will be reported.

Self-examination to see if anything has slipped through the cracks:

```sh
python3 -c "
import json, glob
bad = [(d['exercise'], i) for f in glob.glob('exercises/*/*/checks.json')
       for d in [json.load(open(f))]
       for i, s in enumerate(d['steps'], 1)
       if s['args'] and s['args'][0] == 'touch' and '-t' not in s['args']]
print(bad)"
```

## Only regenerate one topic

```sh
python3 tools/generate_exercises.py --topic 03_variables
./makefiling verify --topic 03_variables
./makefiling selftest --topic 03_variables
```

`--topic` will only import the corresponding specification file, so multiple topics can be written in parallel.

## Do not manually edit files

`exercises/`, `solutions/`, `templates/`, each topic `exercises/<topic>/README.md`
and `docs/curriculum.md` are generated products. To modify them, change
`tools/specs_*.py` and then regenerate. in CI
`python3 tools/generate_exercises.py --check` will reject inconsistent commits.