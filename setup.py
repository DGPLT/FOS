# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : build.py & Last Modded : 2023.07.09. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
https://github.com/mobiusklein/cython_pyinstaller_example/tree/master
https://github.com/ymd-h/exodide
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from pip._internal.cli.main import main as pip
try:
    import exodide
except ModuleNotFoundError:
    pip(["install", "Cython~=3.0.0b", "exodide[all]"])
    #pip(["install", "Cython~=3.0.0b", "git+https://github.com/DOOPLNS/exodide.git"])  # if error occurs

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from exodide import build
import glob
import json
import sys
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


EMCC = False

if "emcc" in sys.argv:
    sys.argv.remove("emcc")
    os.environ['CC'] = "emcc"
    os.environ['CXX'] = "em++"
    os.environ['LDSHARED'] = "emcc -shared"
    EMCC = True

cython_directives = {
    'embedsignature': True,
}

modules = list(map(lambda x: x.replace("\\", "/"), glob.glob("./**/*.pyx", recursive=True)))
print(modules)
extensions = cythonize([
    Extension(name=fname.split('.')[1][1:].replace("/", "."), sources=[fname[2:]], include_dirs=[])
    for fname in modules
    if './build/' not in fname and './dist/' not in fname and './cpython/' not in fname and './emsdk/' not in fname
], compiler_directives=cython_directives)

requirements = open("requirements_emcc.txt" if EMCC else "requirements.txt", "r+")
dependencies = requirements.read().split("\n")
requirements.close()

with open("./config/info.json") as f_info:
    info = json.load(f_info)

setup(name=info['name'],
      version=info['version'],
      zip_safe=False,  # Without these two options
      include_package_data=True,  # PyInstaller may not find your C-Extensions
      packages=find_packages(),
      install_requires=dependencies,
      cmdclass={'build_ext': build_ext} if not EMCC else {"build": build.build, "build_ext": build.build_ext},
      ext_modules=extensions)
