.PHONY: test

test:
	python3 -m pytest --cov=tuxpkg --cov-fail-under=100
