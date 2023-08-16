import glob
import json
from os.path import basename, splitext
from setuptools import find_packages, setup
import os


os.chdir(os.path.dirname(os.path.realpath(__file__)))

requirements = open("requirements.txt", "r+")
dependencies = requirements.read().split("\n")
requirements.close()

module = [fname.split('.')[1][1:].replace("/", ".") for fname in map(lambda x: x.replace("\\", "/"), glob.glob("./**/*.py", recursive=True))
          if './src/simulator/' in fname or './config/' in fname] + ["main"] + ["main3"]
print(module)

with open("./config/info.json") as f_info:
    info = json.load(f_info)

setup(
    name=info['name'],
    version=info['version'],
    packages=find_packages(),
    install_requires=dependencies,
    py_modules=module,
)
