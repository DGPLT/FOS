# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : locations.py & Last Modded : 2023.05.18. ###
Coded with Python 3.10 Grammar by Kim, KyoungHun
Description : Target Information Maintainer Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json
import copy

from config.coordinates import coordinates as _coordinates


class TargetList:
    """ Target List contains Targets, Lakes and Bases """

    def __init__(self):
        self._coordinates = copy.deepcopy(_coordinates)

    class _Locations:
        _TYPE = ""

        def __init__(self, coordinates):
            self._coordinates = coordinates

        def __getitem__(self, key): return TargetList.Location(self._coordinates[self._TYPE][key])

        def keys(self): return self._coordinates[self._TYPE].keys()

    class Location:
        """ Coordination Holder Class """
        def __init__(self, loc_dict):
            self._loc_dict = loc_dict

        @property
        def lat(self): return self._loc_dict["latitude"]

        @property
        def long(self): return self._loc_dict["longitude"]

    class Targets(_Locations):
        """ Current Target Information List """

        def __init__(self):
            super().__init__()
            file_path_target = '/' """파일 주소 값"""

            with open(file_path_target, 'r') as fp_target:
                data_target = json.load(fp_target)

        def decrease_success_possiblity(self):


    def to_json(self): return json.dumps(self._coordinates)
