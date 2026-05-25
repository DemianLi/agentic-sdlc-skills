# TDD Per-Cycle Checklist

Run through this checklist for every RED→GREEN→REFACTOR cycle.

```
[ ] Test describes BEHAVIOR, not implementation detail
[ ] Test uses public interface only (no private method access)
[ ] Test would survive an internal refactor without changes
[ ] Watched test FAIL before writing production code
[ ] Failure was for the EXPECTED reason (not a syntax/import error)
[ ] Production code is MINIMAL to pass this one test
[ ] No speculative features added
[ ] Full suite still GREEN after change
```
