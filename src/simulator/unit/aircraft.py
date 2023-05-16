# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : aircraft.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ????
Description : Aircraft Unit Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json

class Aircraft(dict):
    """ Aircraft Information List """

    def __init__(self):
        super().__init__()
        file_path_aircraft = '/' """파일 주소 값"""

        with open(file_path_aircraft, 'r') as fp_aircraft:
            aircraft_target = json.load(fp_aircraft)

    def to_json(self):
        #TODO
        pass



    #TODO: Create some caluculation methods for aircrafts
