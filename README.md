# pyPlayground

Playground in Python3.9x using [ENKI Robot Simulator](https://github.com/enki-community/enki)

![](images/img-01.png "") ![](images/img-02.png "") ![](images/img-03.png "")

![](images/img-04.png "") ![](images/img-05.png "") ![](images/img-06.png "")

![](images/img-07.png "")

## Tested on
+ Linux
    + Debian 11, Python 3.9.2, Qt5.15.2, libbost-python 1.74.0
+ Windows
    + Windows 10, Python 3.9.0, Qt5.12.10, Boost 1.76.0


## Install
### Windows

> pip install https://github.com/titos-carrasco/pyplayground/dist/pyplayground-1.2.2-py3-none-windows.whl

### Linux
> pip install https://github.com/titos-carrasco/pyplayground/dist/pyplayground-1.2.2-py3-none-linux.whl


### Minimal Test
> $ python -m pyplayground.server.Playground


## Build Wheel (developers)
> $ python setup.py --windows bdist_wheel

> $ python setup.py --linux bdist_wheel
