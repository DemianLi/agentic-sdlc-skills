.PHONY: install-hooks scan test

install-hooks:
	git config core.hooksPath .githooks
	@echo "Git hooks activated. Pre-commit alignment gate is now enforced."

scan:
	python3 skills/s0-eval-alignment/scripts/scan.py

test:
	pytest skills/s0-eval-alignment/tests/ -v
