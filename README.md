# wslpy

This is a Python3 library for WSL specific tasks, and you can use the library to do amazing things:

```python
>>> from wslpy import winsys
>>> winsys.PsExec('Get-Host')


Name             : ConsoleHost
Version          : 5.1.18219.1000
InstanceId       : ac0801e1-5d33-459e-b12d-26120c9e202a
UI               : System.Management.Automation.Internal.Host.InternalHostUserI 
                   nterface
CurrentCulture   : en-US
CurrentUICulture : en-GB
PrivateData      : Microsoft.PowerShell.ConsoleHost+ConsoleColorProxy
DebuggerEnabled  : True
IsRunspacePushed : False
Runspace         : System.Management.Automation.Runspaces.LocalRunspace

>>> from wslpy import convert
>>> convert.to_path('/mnt/c/Windows/')
'c:\\Windows\\'
>>>
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
