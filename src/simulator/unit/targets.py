# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : targets.py & Last Modded : 2023.05.18. ###
Coded with Python 3.10 Grammar by Kim, KyoungHun
Description : Target Information Maintainer Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json


class Targets(dict):
    """ Current Target Information List """

    def __init__(self):
        super().__init__()
        file_path_target = '/' """파일 주소 값"""

        with open(file_path_target, 'r') as fp_target:
            data_target = json.load(fp_target)

    def decrease_success_possiblity(self):

    def to_json(self):
        #TODO
        pass
