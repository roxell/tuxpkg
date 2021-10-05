.PHONY: test

all: test style flake8 typecheck

test:
	python3 -m pytest --cov=tuxpkg --cov-report=term-missing --cov-fail-under=100

style:
	black --check .

flake8:
	flake8 --ignore=E501 .


typecheck:
	mypy .
