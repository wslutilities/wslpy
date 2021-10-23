"""
[![pypi](https://flat.badgen.net/pypi/v/wslpy)](https://pypi.org/project/wslpy/)

> `wslpy` is far from complete. the API will change frequently.

This is a Python3 library for WSL specific tasks,
 and you can use it to do something amazing:

```python
>>> import wslpy as wp
>>> wp.is_wsl()
True
>>> wp.exec.cmd('ver')
Microsoft Windows [Version 10.0.18219.1000]
>>> wp.convert.to('/mnt/c/Windows/')
'c:\\Windows\\'
>>>
```

## Installation

you can install from pypi using `pip install wslpy`,
 or install from source using `python3 setup.py install`

## License

<img width="150" src="https://www.gnu.org/graphics/gplv3-with-text-136x68.png">

This project uses [GPLv3](LICENSE) License.

"""
from .__core__.check import is_interop_enabled, is_wsl

__all__ = [
    "is_interop_enabled",
    "is_wsl",
]
