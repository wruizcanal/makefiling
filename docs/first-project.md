# Small project: write Makefile for a small C project

After completing the basic route, open `exercises/12_cookbook/09_full_cookbook/` without reading the answers first.
Try to explain and achieve the following goals:

- `make` builds `build/final_program` (you can add the `all` entry yourself after completion);
- C and C++ source files are generated into object files under `build/`;
- When the header file changes, only the affected objects are recompiled;
- `make clean` deletes the entire `build/`;
- When running twice in succession, the second time will not be recompiled.

To verify run:

```sh
./makefiling run 12_cookbook/09_full_cookbook
```

After completing it, try to write a small project of your own away from the topic: first draw the dependency graph, and then write rules for each edge.
Finally add `all`, `clean` and `.PHONY`. Being able to explain when each target will be rebuilt is better than memorizing the next one
The "universal Makefile" is more important.