#Basic route: first establish the mental model of Make

If you’re new to Make, don’t treat the 177 questions like a test paper at first. Use the following first
20 questions to build a simple model:

```text
target target <- prerequisites prerequisites
                    │
                    └─ recipe is responsible for generating targets
```

Follow four steps for each exercise:

1. First look at `objective` and predict which commands `make` will execute this time.
2. Modify only the files required by the question, and then run `./makefiling run`.
3. If it fails, first read the original stderr of make, and then run `./makefiling hint --level 2`.
4. After passing, explain in your own words "why the recipe was executed or skipped this time".

Start the basic route:

```sh
./makefiling start
./makefiling next --basic
./makefiling run --basic
```

The basic route goes through: first rule, default target, target file, preconditions, dependency chain, increment
Build, variables, automatic variables, `.PHONY` and `all`. Once completed, proceed to other topics; those topics are
Different abstractions of the same model do not require you to memorize syntax.

Increase the prompt level step by step when you need to see more specific prompts:

```sh
./makefiling hint 00_getting_started/01_first_rule --level 1
./makefiling hint 00_getting_started/01_first_rule --level 2
./makefiling hint 00_getting_started/01_first_rule --level 3
```