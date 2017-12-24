
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  test        Runs tests"
	@echo "  test-all    Runs tests using tox"
	@echo "  release     Makes a release"
	@echo "  isort       Runs isort recursively from your current directory"


test:
	@pytest tests --pdb --flake8

coverage:
	@pytest\
		--flake8\
		--verbose\
		--cov graphql_jwt\
		--cov-config .coveragerc\
		--cov-report term\
		--cov-report xml\
		tests

test-all:
	@tox

release:
	@python setup.py sdist upload
	@python setup.py bdist_wheel upload

isort:
	@isort -rc .

.PHONY: help test coverage test-all release isort
