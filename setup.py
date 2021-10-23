from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wslpy',
    version='0.0.13',
    description='Python Library for WSL specific tasks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPLv3',
    packages=['wslpy'],
    install_requires=['netifaces'],
    author='Patrick Wu',
    author_email='me@patrickwu.space',
    keywords=['system', 'WSL', 'Windows 10', 'Windows 11'],
    url='https://github.com/wslutilities/wslpy',
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
