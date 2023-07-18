# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : build.py & Last Modded : 2023.07.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys
import platform


if platform.system() == "Windows":
    os.system(f"TITLE PyInstaller builder")
elif platform.system() == "Linux":
    os.system("sudo apt-get install patchelf")

print("Python Version:", sys.version, flush=True)

os.system(f'"{sys.executable}" -m pip install tinyaes cryptography pyinstaller')
os.system(f'"{sys.executable}" setup.py develop --user')
os.system(f'"{sys.executable}" -m PyInstaller build.spec --noconfirm')

input("\nBuild Finished. Press any key to terminate.")
