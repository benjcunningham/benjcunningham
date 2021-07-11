.PHONY: install quality style

check_dirs := ci

build:
	python ci/build.py

install:
	pip install -r ci/requirements.txt

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black $(check_dirs)
	isort $(check_dirs)
