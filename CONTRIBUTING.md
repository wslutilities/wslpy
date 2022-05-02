# Contributing

We love pull requests from everyone. By participating in this project, you agree to abide by [Code of Conduct](CODE_OF_CONDUCT.md).

> Due to the package not reaching beta phase, this document will only provides you with a general ideas of the styles that is using in this project.

## System Requirements

- WSL2 installed, a.k.a., running Windows 10 1903 or higher. 
- WSL Distributions that come with Python 3.6+;

You can use the following as the IDE:
- VS Code;
- PyCharm(Recommended).

## Setup environment

- installl `gi` using the following guide: <https://pygobject.readthedocs.io/en/latest/getting_started.html>.
- install `make` from your system and `flake8`, `pdoc`, `nose` and `coverage` from your pip.

## Formatting

- Please use **four spaces** for indentation;
- Use `"""` for function commenting;
- se `#` for general commenting.

## Modules to use
- Use `flake8` for linting (`make lint` to lint);
- Use `nose` for testing and `coverage` for code coverage (`make test` to test and generate code test coverage).
