from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wslpy',
    version='0.0.9',
    description='Python Library for WSL specific tasks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPLv3',
    packages=['wslpy'],
    author='callmepk',
    author_email='wotingwu@live.com',
    keywords=['system','WSL','Windows 10'],
    url='https://github.com/wslutilities/wslpy',
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
