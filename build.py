# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : build.py & Last Modded : 2023.07.09. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import platform


if __name__ == "__main__":
    tool = "PyInstaller"

    if platform.system() == "Windows":
        os.system(f"TITLE {tool} builder")
    elif platform.system() == "Linux":
        os.system("sudo apt-get install patchelf")

    py = input("Please Input python keyword : ")
    print("Python Version : ", end='', flush=True)
    if 1 == os.system(f"{py} --version"):
        raise Exception(f"Cannot find ({py}).")

    os.system(f"{py} -m pip install tinyaes cryptography pyinstaller")
    os.system(f"{py} -m PyInstaller build.spec --noconfirm")

    input("\nBuild Finished.")
