# wslpy

[![pypi](https://flat.badgen.net/pypi/v/wslpy)](https://pypi.org/project/wslpy/)

This is a Python3 library for WSL specific tasks, and you can use it to do something amazing:

```python
>>> import wslpy as wp
>>> wp.isWSL
True
>>> wp.winsys.CmdExec('ver')
Microsoft Windows [Version 10.0.18219.1000]
>>> wp.convert.to_path('/mnt/c/Windows/')
'c:\\Windows\\'
>>>
```

## Installation

you can install from pypi using `pip install wslpy`, or install from source using `python3 setup.py install`

## Documentation

`wslpy` is a small library, it consist following functions and constants:

```python
wslpy.isWSL
wslpy.convert.reg_list()
wslpy.convert.from_reg(input)
wslpy.convert.to_path(input, toType = PathConvType.AUTO)
wslpy.winsys.build
wslpy.winsys.branch
wslpy.winsys.long_build
wslpy.winsys.CmdExec(command)
wslpy.winsys.PwShExec(command)
wslpy.winsys.PwShCrExec(command)
```

## License

<img width="150" src="https://www.gnu.org/graphics/gplv3-with-text-136x68.png">

This project uses [GPLv3](LICENSE) License.
