# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : targets.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ??????
Description : Targets
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json

class Targets(dict):
    """ Current Target Information List """

    def __init__(self):
        super().__init__()
        file_path_target = '/' """파일 주소 값"""

        with open(file_path_target, 'r') as fp_target:
            data_target = json.load(fp_target)

    def to_json(self):
        #TODO
        pass
