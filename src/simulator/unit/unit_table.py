# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : unit_table.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ????
Description : Unit Table Management Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json

class UnitTable(dict):
    """ UnitTable Management Class """

    def __init__(self):
        super().__init__()
        file_path_UnitTable = '/' """파일 주소 값"""

        with open(file_path_UnitTable, 'r') as fp_UnitTable:
            data_UnitTable = json.load(fp_UnitTable)

    def to_json(self):
        #TODO
        pass




    #TODO: Create some caluculation methods for unit table
