# venv-kernel #

[![PyPI - latest version](https://img.shields.io/pypi/v/venv-kernel.svg)](https://pypi.org/project/venv-kernel/)
[![PyPI - License](https://img.shields.io/pypi/l/venv-kernel.svg)](https://pypi.org/project/venv-kernel/)
[![PyPI - supported Python versions](https://img.shields.io/pypi/pyversions/venv-kernel.svg)](https://pypi.org/project/venv-kernel/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/venv-kernel)](https://pypi.org/project/venv-kernel/)

## Summary ##

This package creates jupyter kernels for the `venv` it is installed
in.

## Use-case scenario ##

You maintain multiple virtual environments via python's `venv`. You
want to be able to switch between them from within a _single_ jupyter
installation. How do you do this?

You need a (user-) global jupyter installation. The recommended
approach for that is to use `pipx` to install jupyter as a standalone
tool. Jupyter can handle multiple different kernels, even for the same
python version, and they are easily maintained with the `jupyter
kernelspec` command. The only nuissance is to create and install the
kernel.json files manually for each venv. That's where `venv-kernel`
comes in.

## Suggested workflow ##

### One-time setup ###

It is recommended to maintain your python versions with `pyenv` and
jupyter with `pipx`. Both of these packages can be installed with the
usual package managers such as `apt-get` or `brew`.

Specifically, install and temporarily activate a recent python version
with pyenv, e.g., via
```
pyenv install 3.9.10
pyenv shell 3.9.10
```
Then install jupyter using pipx as per
```
pipx install --install-deps notebook jupyter jupyter_contrib_nbextensions
```
which places it in its own virtual environment, all managed by
pipx. You can call jupyter from the command line now.

### Install a custom kernel for a VENV ###

Every time you want to add a custom virtual environment as a kernel
option to your jupyter notebook server, follow these steps:

1. If you haven't done so yet, create and activate the venv as per usual, e.g., via
    ```bash
    pyenv shell 3.10 # we want to use this particular python version
    pip -m venv .venv
    . .venv/bin/activate
    pip install --upgrade pip
    pip install <list of packages here> or pip install -r requirements.txt
    ```
2. Install venv-kernel as per
    ```bash
    pip install venv-kernel
    ```
3. Create and install the custom jupyter kernel
    ```bash
    venv-kernel install --name "MyProject" --description "Virtual Environment for MyProject using Python 3.10"
    ```
   Here the `--name` and `--description` are optional and default
   to the direcory name of the virtual environment.
4. Start/restart your jupyter notebook server. You should now see the
   kernel "MyProject", which uses the Python version of your virtual
   environment and has access to all the packages installed in it.
    
### Removal ###
    
If for any reason you want to uninstall a kernel created by this
package, you can simply do so using the commands
```bash
jupyter kernelspec list
```
to identify the kernel in question
and then delete it via 
```bash
jupyter kernelspec remove
```

If you are within a virtualenv that has `venv-kernel` installed, you
can also use
```bash
venv-kernel list
```
to see if there's currently a kernel installed that corresponds to the current venv, and 
```bash
venv-kernel clean
```
to remove it.

## Similar packages ##
    
There are other packages that provide similar or related
functionality, and these may or may not serve your purposes better
than this package, which is designed solely to meet the author's
needs. These packages include:

- [callisto](https://pypi.org/project/callisto/): Create jupyter kernels from virtual environments
- [envkernel](https://pypi.org/project/envkernel/): Jupyter kernels manipulation and in other environments (docker, Lmod, etc.)
- [ssh-ipykernel](https://pypi.org/project/ssh-ipykernel/): A remote jupyter ipykernel via ssh
    
## MIT License ##

Copyright 2021 Björn Rüffer

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



    
