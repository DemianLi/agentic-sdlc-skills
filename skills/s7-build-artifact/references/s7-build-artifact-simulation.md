# s7-build-artifact — Simulation Mode & Monorepo Notes

## Simulation Mode

If no registry configured (trial context), artifact lives in `dist/` and git tag is local only. Document as `deploy_target: "local"`.

Do NOT push to PyPI / Docker Hub / npm unless explicitly instructed.

## Monorepo Caveat

If trial project in larger repo subdirectory, `git tag` tags monorepo root, not trial project. Skip git tag step; note `git_tag: "skipped (monorepo context)"`. Git tags only make sense when repo root = project root.
