# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : aircraft.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Kim, KyoungHun
Description : Aircraft Unit Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from config.aircraft_spec_sheet import spec_sheet


class Aircraft:
    """ Aircraft Information List """

    class BasicAircraft:
        _cover_area_types = (0, 1, 2)
        _aircraft_types = {"Drone": "Drone", "Helicopter": "Helicopter", "Airplane": "Airplane"}

        def __init__(self, dictionary):
            self._type: str = self._aircraft_types[dictionary["Aircraft Type"]]
            self._velocity: int = int(dictionary["Velocity"])
            self._etrdy: int = int(dictionary["ETRDY"])
            self._cost: int = int(dictionary["Cost"])
            self._area: int = self._cover_area_types[int(dictionary["Cover Area"])]
            self._tank: float = float(dictionary["Water Tank"])
            self._poss: int = int(dictionary["Possibility"])
            if not (0 <= self._poss <= 100):
                raise ValueError("Possibility must be between 0 and 100.")

        @property
        def type(self) -> str:
            return self._type

        @property
        def velocity(self) -> int:
            return self._velocity

        @property
        def ETRDY(self) -> int:
            return self._etrdy

        @property
        def cost(self) -> int:
            return self._cost

        @property
        def cover_area(self) -> int:
            return self._area

        @property
        def possibility(self) -> int:
            return self._poss

        def get_expected_percentage_of_water_by_min(self, percentage: float) -> float:
            """ Returns the estimated water percentage by time """
            return   #TODO: fill this

        def get_water_fill_time_by_current_percentage(self, percentage: float) -> float:
            """ Returns the estimated water filling (100%) time from the current water percentage """
            return int(self._tank * (1-0.01*percentage) * 10) / 10  #TODO: need to check it this work fine

    _aircraft_list = {
        key: BasicAircraft(val) for key, val in spec_sheet.items()
    }

    @classmethod
    def __getitem__(cls, key):
        return cls._aircraft_list[key]

    @classmethod
    def keys(cls):
        return cls._aircraft_list.keys()

    @staticmethod
    def to_json():
        return spec_sheet
