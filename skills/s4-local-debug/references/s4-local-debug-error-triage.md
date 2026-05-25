# s4-local-debug — Error Type Triage

| Error | First Action |
|------|--------------|
| Build | Read first error; fix; re-run |
| Type error | Check at source, not use point |
| Test failure | Read diff: actual vs. expected |
| Runtime panic | Read top stack frame |
| Flaky test | Run 3× — inconsistent? NEEDS_CONTEXT |
| Dependency version | Check lock file vs. installed |
