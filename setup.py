# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : build.py & Last Modded : 2023.07.09. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
https://github.com/mobiusklein/cython_pyinstaller_example/tree/master
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import glob

cython_directives = {
    'embedsignature': True,
}

extensions = cythonize([
    Extension(name=fname.split('.')[1][1:].replace("/", "."), sources=[fname[2:]], include_dirs=[])
    for fname in map(lambda x: x.replace("\\", "/"), glob.glob("./**/*.pyx", recursive=True))
    if './build/' not in fname and './dist/' not in fname
], compiler_directives=cython_directives)

setup(name="fos_simulator",
      version="1.0.0.0",
      zip_safe=False,  # Without these two options
      include_package_data=True,  # PyInstaller may not find your C-Extensions
      packages=find_packages(),
      ext_modules=extensions)
