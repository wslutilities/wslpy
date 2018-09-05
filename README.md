# wslpy

This is a Python3 library for WSL specific tasks, and you can use it to do something amazing:

```python
>>> from wslpy import winsys
>>> winsys.isWSL
True
>>> winsys.CmdExec('ver')
Microsoft Windows [Version 10.0.18219.1000]
>>> from wslpy import convert
>>> convert.to_path('/mnt/c/Windows/')
'c:\\Windows\\'
>>>
```

## Installation

run `pip3 install wslpy`, or install from source:

```bash
python3 setup.py install
```

## Documentation

After installation, you can import the library using `import wslpy`, or import individual class in following way:

```python
from wslpy import convert
from wslpy import winsys
```

`wslpy` is a small library, it consist following functions and constants:

```python
wslpy.convert.reg_list()
wslpy.convert.from_reg(input)
wslpy.convert.to_path(input, toType = PathConvType.AUTO)
wslpy.winsys.build
wslpy.winsys.branch
wslpy.winsys.long_build
wslpy.winsys.CmdExec(command)
wslpy.winsys.PsExec(command)
```

## License

LGPL 3.0.
