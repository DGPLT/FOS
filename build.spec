# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import re
import subprocess


debug_mode = False
console_mode = True


# GET CRYTO KEY
key_path = "build.key"
if not os.path.isfile(key_path):
    print("ERROR: build.key not found", flush=True)
    if input("Do you want to create a new encryption key? (y to yes) : ") == 'y':
        print("Generating new key...", flush=True)
        from cryptography.fernet import Fernet
        key = Fernet.generate_key().decode()[-16:]
        with open(key_path, "wt", encoding='utf-8') as f:
            f.write(key)
    else:
        while True:
                key = input("Please enter the encryption 16-digit key: ")
                if len(key) == 16:
                    with open(key_path, "wt", encoding='utf-8') as f:
                        f.write(key)
                    break
                else:
                    print("ERROR: Key entered is not 16 digits.")
with open("build.key", "rt", encoding='utf-8') as f:
    CRYPTO_KEY = f.read()
block_cipher = pyi_crypto.PyiBlockCipher(key=CRYPTO_KEY)


# EXE Settings
__NAME__ = "FOS Simulator"
__PRODUCT_NAME__ = "FOS Simulator - Desktop Version"
__DESCRIPTION__ = "Operation Simulation Game for AI/ML Learning"
__VERSION__ = "1.0.0.0"
__VER_SPL__ = __VERSION__.split('-')[0].split('.')[:4]
__COPYRIGHT__ = "MIT License"
__COMPANY_NAME__ = "USFK J5 Digital O-Plan"


# CREATE VERSION.RC FILE
version = f"""# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=({__VER_SPL__[0]}, {__VER_SPL__[1]}, {__VER_SPL__[2]}, {__VER_SPL__[3]}),
prodvers=({__VER_SPL__[0]}, {__VER_SPL__[1]}, {__VER_SPL__[2]}, {__VER_SPL__[3]}),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x40004,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'{__COMPANY_NAME__}'),
    StringStruct(u'FileDescription', u'{__DESCRIPTION__}'),
    StringStruct(u'FileVersion', u'{__VERSION__}'),
    StringStruct(u'InternalName', u'{__NAME__}'),
    StringStruct(u'LegalCopyright', u'{__COPYRIGHT__}'),
    StringStruct(u'OriginalFilename', u'{__NAME__}.exe'),
    StringStruct(u'ProductName', u'{__PRODUCT_NAME__}'),
    StringStruct(u'ProductVersion', u'{__VERSION__}')])
  ]),
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
if not os.path.isdir('build'):
    os.mkdir('build')
with open('build/version.rc', 'wt', encoding='utf-8') as f:
    f.write(version)


# INCLUDE OR EXCLUDE MODULES
installed_packages = re.split(r"[\r\n]", subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8'))
PACKAGES = ['cryptography', 'tinyaes']
with open("requirements.txt", "rt", encoding='utf-8') as f:  # include
    requirements = [re.split(r"[~=<>]", pkg)[0] for pkg in f.readlines() if pkg != '' and pkg != '\n']
    PACKAGES.extend(requirements)
print("Included packages : ", PACKAGES)
HIDDEN_IMPORTS = ['os', 'sys', 're']
print("Included packages (HIDDEN) : ", HIDDEN_IMPORTS)
EXCLUDES = list(set([pkg.split('==')[0] for pkg in installed_packages if pkg != ''] + ['tkinter']) - set(PACKAGES) - set(HIDDEN_IMPORTS))
print("Excluded packages : ", EXCLUDES, end="\n\n")


# BUILD
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[('res', 'res')],
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

#a.datas += [('icon.ico', 'icon.ico', 'DATA')
#			]  # some files to add (--add-data option)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if input("\n\nArchive as a exe file? (y to yes) : ") == "y":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=__NAME__,
        debug=debug_mode,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=console_mode,
        icon='res/icon.ico',
        version='build/version.rc',
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=__NAME__,
        debug=debug_mode,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=console_mode,
        icon='res/icon.ico',
        version='build/version.rc',
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name=__NAME__
    )
