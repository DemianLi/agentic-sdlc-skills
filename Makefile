.PHONY: install-hooks scan test status next

install-hooks:
	git config core.hooksPath .githooks
	@echo "Git hooks activated. Pre-commit alignment gate is now enforced."

scan:
	python3 skills/s0-eval-alignment/scripts/scan.py

test:
	pytest skills/s0-eval-alignment/tests/ -v

status:
	python3 skills/s0-eval-alignment/scripts/engine.py --mode fluid --status

next:
	python3 skills/s0-eval-alignment/scripts/engine.py --next

