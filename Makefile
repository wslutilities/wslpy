PYTHON := python3

lint:
	$(PYTHON) -m flake8 wslpy/

build:
	$(PYTHON) setup.py bdist bdist_wheel
