from setuptools import setup
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wslpy',
    version='0.2.0',
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
    ],
    cmdclass=cmdclass,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'wslpy'),
            'version': ('setup.py', '0.2'),
            'release': ('setup.py', '0.2.0'),
            'source_dir': ('setup.py', 'docsources')}},
)
