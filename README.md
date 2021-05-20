# wslpy

[![pypi](https://flat.badgen.net/pypi/v/wslpy)](https://pypi.org/project/wslpy/)

> `wslpy` is far from complete. the API will change frequently.

This is a Python3 library for WSL specific tasks, and you can use it to do something amazing:

```python
>>> import wslpy as wp
>>> wp.isWSL()
True
>>> wp.exec.cmd('ver')
Microsoft Windows [Version 10.0.18219.1000]
>>> wp.convert.to('/mnt/c/Windows/')
'c:\\Windows\\'
>>>
```

## Installation

you can install from pypi using `pip install wslpy`, or install from source using `python3 setup.py install`

## Documentation

> `wslpy` is far from complete. this documentation page will change frequently.

`wslpy` is a small library, it consist following functions and constants:

```python
wslpy.isWSL()
wslpy.system.shellEnvVarList()
wslpy.system.registry(input)
wslpy.convert.to(input, toType=PathConvType.AUTO)
wslpy.convert.toWin(input) 
wslpy.convert.toWinDouble(input)
wslpy.convert.toWSL(input) 
wslpy.exec.cmd(command)
wslpy.exec.pwSh(command)
wslpy.exec.pwShCr(command)
```

## License

<img width="150" src="https://www.gnu.org/graphics/gplv3-with-text-136x68.png">

This project uses [GPLv3](LICENSE) License.
