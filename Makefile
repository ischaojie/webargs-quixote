.DEFAULT_GOAL := all
isort = isort webargs_quixote tests
black = black webargs_quixote tests

.PHONY: check
check:
	flake8 webargs_quixote/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: lint
lint:
	$(isort)
	$(black)

.PHONY: test
test:
	pytest tests/ --cov=webargs_quixote

.PHONY: coverage
coverage:
	coverage report --show-missing --skip-covered --fail-under=90
	coverage xml
	coverage html

.PHONY: publish
publish:
	poetry publish --build
