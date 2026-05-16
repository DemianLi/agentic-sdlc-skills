# Project Context: slugify

**Date**: 2026-05-16
**Skill**: s1-config-context
**Stage**: s1

---

## Domain Terms

| Term | Definition |
|---|---|
| **slug** | A URL-safe string consisting only of lowercase ASCII letters, digits, and a separator character; used in web URLs to represent human-readable identifiers |
| **separator** | The character inserted in place of whitespace when converting text to a slug; default is hyphen (`-`) |
| **slugify** | The transformation process: lowercase input, replace spaces with separator, strip all characters that are not `[a-z0-9<separator>]` |
| **strip** | Removal of characters outside the allowed set `[a-z0-9<sep>]` — not replacement, complete removal |
| **empty-after-strip** | Condition where the resulting slug is an empty string after applying lowercase, separator substitution, and character removal; triggers exit code 1 |
| **stdin mode** | CLI behaviour when no positional TEXT argument is given: reads the entire standard input stream until EOF and slugifies it |

---

## AI Boundaries

### Autonomous (no confirmation required)
- Read and parse text input from arguments or stdin
- Apply slugify transformation (lowercase, replace, strip)
- Write slug output to stdout
- Run tests and report results
- Create or modify files within the `test_projects/trial-15-gates/` directory

### Requires explicit user confirmation
- Writing to directories outside `test_projects/trial-15-gates/`
- Publishing to PyPI or any external package registry
- Changing the default separator character from `-`
- Modifying the character allowlist `[a-z0-9<sep>]`
