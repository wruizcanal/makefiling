"""Shared data structures for the makefiling exercise generator.

Each exercise is described once, here.  The generator turns a spec into three
trees of files:

*``solutions/``  the correct Makefile and its supporting files
*``exercises/``  the same thing with the spec's ``breaks`` applied
*``templates/``  a byte-identical copy of ``exercises/``, used by ``reset``

The third file every exercise directory carries is ``checks.json``.  It is the
machine-readable contract for the exercise: a list of steps, each one a command
to run plus what the result must look like.  The runner (``./makefiling``) is
nothing more than an interpreter for that file.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# How a step's captured output is compared with the expectation.
#
#   exact          the whole output must match
#   contains       the output must contain the given text
#   contains_lines every line of the expectation must appear, in any order
#   ordered_lines  every line must appear, in the given order
#   regex          the expectation is a regular expression searched in the output
#   not_contains   the output must not contain the given text
MATCH_MODES = (
    "Exact",
    "Contains",
    "Contains lines",
    "Ordered lines",
    "Regex",
    "Not contains",
)


# A short, model-first route for absolute beginners.  The complete catalogue
# remains available, but these lessons make the first twenty exercises feel
# like one story: predict the dependency graph, run make, then explain why it
# did (or did not) run a recipe.
BASIC_LESSONS: dict[str, dict[str, object]] = {
    "00 getting started/01 first rule": {
        "Order": 1,
        "Goal": "Let make execute the simplest recipe.",
        "Prediction": "Which target will be read when running make? Does the terminal display the command first, or only the output of the command?",
        "Hints": [
            "The rule consists of the target line and recipe: hello: The next line is the command to be executed.",
            "The recipe line must start with a real TAB.",
            "Place the echo command below hello: and indent it with TAB.",
        ],
        "Explanation": "make builds the first target by default; the recipe will be echoed first and then handed over to the shell for execution.",
    },
    "00 getting started/02 default goal": {
        "Order": 2,
        "Goal": "Understand the difference between default and explicit goals.",
        "Prediction": "Which rule will be chosen by naked make and make goodbye respectively?",
        "Hints": [
            "When there are no command-line targets, make chooses the first target it reads.",
            "When moving the entire rule, the target name and its recipe are moved together.",
            "Let the hello rule appear before goodbye.",
        ],
        "Explanation": "Naked make only builds the first target; explicitly writing goodbye will select goodbye.",
    },
    "00 getting started/03 essence target file": {
        "Order": 3,
        "Goal": "Observe how the target names correspond to files on disk.",
        "Prediction": "After the first make, why does the second make no longer execute echo?",
        "Hints": [
            "make determines whether hello already exists through the file system.",
            "The recipe must actually create a file named hello.",
            "Redirect the output of echo to hello.",
        ],
        "Explanation": "When the target file exists and there are no later preconditions, make considers the target to be up to date.",
    },
    "00 getting started/04 essence prerequisites": {
        "Order": 4,
        "Goal": "Use preconditions to express \"the source file needs to be rebuilt after changes\".",
        "Prediction": "After only modifying blah.c, will make execute cc again?",
        "Hints": [
            "List the files it depends on to the right of the colon after the target name.",
            "blah should depend on blah.c.",
            "make compares the modification times of targets and preconditions.",
        ],
        "Explanation": "Make will execute the recipe only if the target does not exist, or if any of the preconditions are newer than the target.",
    },
    "00 getting started/05 which makefile": {
        "Order": 5,
        "Goal": "Know how make selects Makefiles.",
        "Prediction": "When both GNUmakefile and Makefile exist in the directory, who does bare make read?",
        "Hints": [
            "GNU Make has a fixed filename search order.",
            "make -f filename can skip the default search.",
            "Let the two files output different text, and then use three check commands to compare.",
        ],
        "Explanation": "GNUmakefile has higher priority than makefile and Makefile; -f can be specified explicitly.",
    },
    "00 getting started/06 beyond compilation": {
        "Order": 6,
        "Goal": "Think of make as a dependency graph executor, not just a compiler wrapper.",
        "Prediction": "When making report, what is the order of summary.txt and report?",
        "Hints": [
            "The report recipe reads summary.txt, so report should rely on it.",
            "summary.txt in turn depends on names.txt.",
            "Write dependencies on the right side of the colon, recipe is only responsible for actions.",
        ],
        "Explanation": "make recursively builds preconditions before executing the target recipe; any command can become a recipe.",
    },
    "01 syntax and essence/01 rule anatomy": {
        "Order": 7,
        "Goal": "Unpack a rule's goals, preconditions, and recipes.",
        "Prediction": "Will make report.txt check notes.txt first, or run the two commands directly?",
        "Hints": [
            "The rule header is of the form target: prerequisites.",
            "Two recipes can be written consecutively under the same target.",
            "The second command must also begin with TAB.",
        ],
        "Explanation": "Target lines describe dependencies, and each indented line belongs to the recipe.",
    },
    "01 syntax and essence/02 several targets one rule": {
        "Order": 8,
        "Goal": "Have one rule serve multiple target names.",
        "Prediction": "When requesting two targets separately, can make execute the same recipe?",
        "Hints": [
            "Multiple goals can be written to the left of the same colon.",
            "Target names are separated by spaces.",
            "Don't write the second goal as a precondition.",
        ],
        "Explanation": "The same rule can provide the same recipe to multiple targets; the list of targets remains to the left of the colon.",
    },
    "01 syntax and essence/03 prerequisite order": {
        "Order": 9,
        "Goal": "Observe that make traverses the graph in dependency order.",
        "Prediction": "When all: one two three, what is the output order of the three recipes?",
        "Hints": [
            "The precondition of all is the entry point of the construction sequence.",
            "Write one, two, and three to the right of the colon in the desired order.",
            "The output order of recipes can help you verify your dependency graph.",
        ],
        "Explanation": "make will first process the preconditions and then return to the target; preconditions at the same level are accessed in the order of writing.",
    },
    "01 syntax and essence/04 recipe creates the target": {
        "Order": 10,
        "Goal": "Let recipe create the target file it declares.",
        "Prediction": "If recipe creates hello, what happens the second time make?",
        "Hints": [
            "Whether the target is up to date depends on whether a file with the same name exists.",
            "Write two lines of text to hello instead of just printing to the terminal.",
            "You can use echo in combination with > and >> to write files.",
        ],
        "Explanation": "The side effect of the recipe must match the target name, otherwise make will have to try again every time.",
    },
    "01 syntax and essence/05 timestamps decide": {
        "Order": 11,
        "Goal": "Understanding incremental builds with timestamps.",
        "Prediction": "Will the source file be rebuilt if it is older than the target? What about after the source file is updated?",
        "Hints": [
            "The target requires a source file as a prerequisite.",
            "make only cares about the modification time and does not understand the file content.",
            "First make sure blah.c is older, then make it newer and observe the results twice.",
        ],
        "Explanation": "Make's default incremental strategy is: if the target is missing or any dependency is updated, rebuild the target.",
    },
    "01 syntax and essence/06 every prerequisite counts": {
        "Order": 12,
        "Goal": "Understanding any of several preconditions can trigger a rebuild.",
        "Prediction": "If only a.txt is updated or only b.txt is updated, will combined.txt be rebuilt?",
        "Hints": [
            "All dependencies are written to the right of the colon on the same target line.",
            "In the absence of b.txt, make will not know that it participated in the build.",
            "The recipe can continue to read both files as needed.",
        ],
        "Explanation": "The target must be newer than all preconditions; any new dependency will make the target out of date.",
    },
    "02 quick examples/01 three step chain": {
        "Order": 13,
        "Goal": "Build a three-tier dependency chain.",
        "Prediction": "When building blah from an empty directory, what is the order of blah.c, blah.o, blah?",
        "Hints": [
            "The final goal blah depends on blah.o, and blah.o depends on blah.c.",
            "Each level requires a rule.",
            "Draw an arrow downward from the final goal and then execute it in the opposite direction.",
        ],
        "Explanation": "Make recursively walks through the entire dependency chain, and then executes the recipe from the bottom.",
    },
    "02 quick examples/03 touching an intermediate file": {
        "Order": 14,
        "Goal": "Observe that only the affected chain segments are rebuilt.",
        "Prediction": "Will blah.c be recompiled when only blah.o is updated?",
        "Hints": [
            "blah.o must declare blah.c as a dependency.",
            "The final goal blah depends on blah.o.",
            "Compare each output to find recipes that have not been re-executed.",
        ],
        "Explanation": "Incremental builds only execute the portion of the recipe required to get from the expired node to the final target.",
    },
    "02 quick examples/08 clean can run twice": {
        "Order": 15,
        "Goal": "Use clean to restore the build product to a rebuildable state.",
        "Prediction": "When clean is run twice, should it fail or succeed the second time?",
        "Hints": [
            "clean usually does not produce a file named clean.",
            "rm -f continues to succeed even if the file does not exist.",
            "clean is an action target, not a build product.",
        ],
        "Explanation": "clean is responsible for deleting artifacts; idempotent clean commands can be safely executed repeatedly.",
    },
    "02 quick examples/10 build clean build": {
        "Order": 16,
        "Goal": "Complete experience build → clean → build.",
        "Prediction": "If you build again after cleaning, which recipes will be re-executed?",
        "Hints": [
            "clean must remove all artifacts created by this set of exercises.",
            "Build once, clean again, observe a third time.",
            "If any files remain, make will treat them as existing targets.",
        ],
        "Explanation": "After clean deletes the target, make will re-walk the entire dependency chain next time.",
    },
    "03 variables/01 a list in a variable": {
        "Order": 17,
        "Goal": "Use variables to name the same set of files.",
        "Prediction": "How does make expand when $(files) appears in the target line and recipe?",
        "Hints": [
            "The variable definition is in the form files := file1 file2.",
            "some_file should put files to the right of the colon.",
            "You can also write $(files) directly in the recipe.",
        ],
        "Explanation": "The variable is first expanded into text; in the dependency list, it becomes multiple file names.",
    },
    "03 variables/09 the four common automatic variables": {
        "Order": 18,
        "Goal": "Understand the most commonly used automatic variables in recipes.",
        "Prediction": "What do $@, $<, $^, $? stand for respectively?",
        "Hints": [
            "$@ is the current target and $< is the first precondition.",
            "$^ are all preconditions, $? are those newer than the target.",
            "Automatic variables only have meaning when the recipe is executed.",
        ],
        "Explanation": "Automatic variables are populated by make based on the current rule context and do not need to be defined manually.",
    },
    "04 targets/03 phony clean": {
        "Order": 19,
        "Goal": "Understand how .PHONY declares action targets.",
        "Prediction": "When there is already a file called clean in the directory, will make clean delete the product?",
        "Hints": [
            "By default, make treats the target name as a possible existing file.",
            ".PHONY: clean tells make clean to never be a file.",
            "You can put the .PHONY statement before or after the clean rule.",
        ],
        "Explanation": "The .PHONY target does not participate in file timestamp determination and will be executed every time it is requested.",
    },
    "04 targets/04 all builds everything": {
        "Order": 20,
        "Goal": "Use all as an aggregation target.",
        "Prediction": "When using bare make, will all three preconditions of all be built?",
        "Hints": [
            "all is a common target, just a conventional general entry.",
            "List one, two, and three as preconditions for all.",
            "Let all be the first target in the file.",
        ],
        "Explanation": "all itself can have no recipe; it aggregates multiple independent targets through preconditions.",
    },
}


@dataclass(frozen=True)
class Step:
    """One command to run in the exercise directory, and what it must produce.

    ``args`` is a complete argv, so a step can invoke ``make`` with any flags,
    run ``./script.sh``, or call a tool that ``make`` itself is expected to
    have produced.  ``argv[0]`` is resolved on ``PATH``.
    """

    args: list[str]
    description: str = ""
    exit_code: int = 0
    stdout: str | None = None
    stdout_mode: str = "Contains lines"
    stderr: str | None = None
    stderr_mode: str = "Contains"
    env: dict[str, str] = field(default_factory=dict)
    #: Files that must exist after the step, with exactly this content.
    files: dict[str, str] = field(default_factory=dict)
    #: Paths that must not exist after the step.
    missing: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "Args": list(self.args),
            "Description": self.description,
            "Exit code": self.exit_code,
            "Stdout": self.stdout,
            "Stdout mode": self.stdout_mode,
            "Stderr": self.stderr,
            "Stderr mode": self.stderr_mode,
            "Env": dict(self.env),
            "Files": dict(self.files),
            "Missing": list(self.missing),
        }


@dataclass(frozen=True)
class ExerciseSpec:
    topic: str
    slug: str
    title: str
    objective: str
    reference: str
    hint: str
    #: The correct Makefile, as it ends up in ``solutions/``.
    makefile: str
    steps: list[Step]
    #: ``(correct, learner)`` replacements that turn the Makefile into the
    #: exercise.  At least one is required: an exercise that already passes
    #: would make ``selftest`` fail.
    breaks: list[tuple[str, str]] = field(default_factory=list)
    #: Extra files copied next to the Makefile, keyed by relative path.
    files: dict[str, str] = field(default_factory=dict)
    #: ``(filename, correct, learner)`` replacements applied to ``files``.
    file_breaks: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def ident(self) -> str:
        return f"{self.topic}/{self.slug}"


def ex(
    topic: str,
    slug: str,
    title: str,
    objective: str,
    reference: str,
    hint: str,
    makefile: str,
    steps: list[Step],
    breaks: list[tuple[str, str]],
    files: dict[str, str] | None = None,
    file_breaks: list[tuple[str, str, str]] | None = None,
) -> ExerciseSpec:
    """Describe one exercise.

    ``makefile`` and every entry in ``files`` are stripped of leading and
    trailing blank lines and end with exactly one newline, so specs can use
    triple-quoted strings without worrying about the surrounding whitespace.
    Recipe lines inside ``makefile`` must be indented with a real tab.
    """
    return ExerciseSpec(
        topic=topic,
        slug=slug,
        title=title,
        objective=objective,
        reference=reference,
        hint=hint,
        makefile=clean(makefile),
        steps=steps,
        breaks=breaks,
        files={name: clean(content) for name, content in (files or {}).items()},
        file_breaks=file_breaks or [],
    )


def mk(*args: str, **kwargs: object) -> Step:
    """A step that runs ``make`` with the given arguments."""
    return step("Make", *args, **kwargs)


def step(cmd: str, *args: str, **kwargs: object) -> Step:
    """A step that runs ``cmd`` with the given arguments.

    Keyword arguments map onto :class:`Step` fields.  ``stdout`` (or
    ``stderr``) may be passed together with the matching ``*_mode``; passing
    ``stdout`` alone means "these lines must all appear, in this order".
    """
    if "Stdout" in kwargs and "Stdout mode" not in kwargs:
        kwargs["Stdout mode"] = "Ordered lines"
    return Step(args=[cmd, *args], **kwargs)  # type: ignore[arg-type]


def clean(text: str) -> str:
    """Normalise a spec string: no surrounding blank lines, one final newline."""
    return text.strip("\n") + "\n"


def checks_document(spec: ExerciseSpec) -> dict[str, object]:
    """The contents of ``checks.json`` for an exercise."""
    document = {
        "Exercise": spec.ident,
        "Title": spec.title,
        "Objective": spec.objective,
        "Reference": spec.reference,
        "Hint": spec.hint,
        "Steps": [s.to_json() for s in spec.steps],
    }
    lesson = BASIC_LESSONS.get(spec.ident)
    if lesson:
        document["Lesson"] = lesson
    return document
