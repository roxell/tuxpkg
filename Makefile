.PHONY: test

all: typecheck test style flake8

test:
	python3 -m pytest --cov=tuxpkg --cov-report=term-missing --cov-fail-under=100

style:
	black --check .

flake8:
	flake8 --exclude=dist/ --ignore=E501 .

typecheck:
	mypy --exclude=dist/ .

export PROJECT := tuxpkg
include tuxpkg/data/tuxpkg.mk
