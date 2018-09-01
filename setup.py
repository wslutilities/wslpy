from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wslpy',
    version='0.0.1',
    description='Python Library for WSL specific tasks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['wslpy'],
    author='callmepk',
    author_email='wotingwu@live.com',
    install_requires=[],
    keywords=['system','WSL','Windows 10'],
    url='https://github.com/wslutilities/wslpy'
)
