PYTHON := python3

lint:
	$(PYTHON) -m flake8 --exclude tests wslpy/

test:
	rm -rf htmlcov
	nosetests --with-coverage --cover-erase --cover-package=wslpy -w wslpy/
	coverage html

build:
	$(PYTHON) setup.py bdist bdist_wheel
