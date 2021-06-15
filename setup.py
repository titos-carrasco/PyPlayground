# {dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl

from setuptools import setup
import sys

SETUP = {
    "name"             : "pyplayground",
    "version"          : "1.2.5",
    "description"      : "Controlling robots in the ENKI Robot Simulator",
    "license"          : "MIT",
    "author"           : "Roberto Carrasco",
    "author_email"     : "titos.carrasco@gmail.com",
    "maintainer"       : "Roberto Carrasco",
    "maintainer_email" : "titos.carrasco@gmail.com",
    "packages"         : [
                            "pyplayground",
                            "pyplayground.client",
                            "pyplayground.server"
                         ],
    "package_dir"      : { "pyplayground.server": "pyplayground/server" },
    "package_data"     : { "pyplayground.server": [ "example.*" ] },
}

if( "--windows" in sys.argv ):
    sys.argv.remove( "--windows" )
    sys.argv.append( "--plat-name=win_amd64" )
    data_files = [
                    "pyenki.pyd",
                    "*.dll",
                    "winqt/iconengines/*",
                    "winqt/imageformats/*",
                    "winqt/platforms/*",
                    "winqt/styles/*",
                    "winqt/translations/*"
                  ]
    SETUP["package_data"]["pyplayground.server"] += data_files

elif( "--linux" in sys.argv ):
    #manylinux1     x86-64
    sys.argv.remove( "--linux" )
    sys.argv.append( "--plat-name=linux-x86_64" )
    data_files = [
                    "pyenki.so"
                 ]
    SETUP["package_data"]["pyplayground.server"] += data_files

else:
    SETUP = {}


setup( **SETUP )
