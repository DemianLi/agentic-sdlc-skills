# TDD Red Flags — Full Table

| Rationalization | Reality |
|----------------|---------|
| "I'll write tests after" | Tests after pass immediately — prove nothing. |
| "Deleting X hours of work is wasteful" | Sunk cost. Unverified code is the real waste. |
| "Tests after achieve the same goals" | After: "what does this do?" First: "what SHOULD this do?" |
| Code exists before test / passes immediately / can't explain failure | DELETE and restart |
| "Too simple to test" | Simple code breaks. The test documents expected behavior. |
| "I already manually tested it" | Ad-hoc ≠ systematic. Reproducibility is the whole point. |
| "This is too complex to test" | Hard to test = hard to use. Your design is the problem. |
