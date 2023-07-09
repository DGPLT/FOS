# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : aircraft.py & Last Modded : 2023.05.18. ###
Coded with Python 3.10 Grammar by Kim, KyoungHun
Description : Aircraft Unit Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from __future__ import annotations

from enum import Enum
import json

from config.aircraft_spec_sheet import spec_sheet

_cached_json = json.dumps(spec_sheet)


class BasicAircraft:
    class CoverArea(Enum):
        NONE = 0
        ONE_TILE = 1
        DIAGONAL = 2

    class Type(Enum):
        Drone = "Drone"
        Helicopter = "Helicopter"
        Airplane = "Airplane"

    def __init__(self, dictionary):
        Type, CoverArea = self.Type, self.CoverArea
        self._type: Type = Type(dictionary["Aircraft Type"])
        self._velocity: int = int(dictionary["Velocity"])
        self._etrdy: int = int(dictionary["ETRDY"])
        self._cost: int = int(dictionary["Cost"])
        self._area: CoverArea = CoverArea(int(dictionary["Cover Area"]))
        self._tank: float = float(dictionary["Water Tank"])
        self._poss: int = int(dictionary["Possibility"])
        if not (0 <= self._poss <= 100):
            raise ValueError("Possibility must be between 0 and 100.")

    @property
    def type(self) -> Type: return self._type

    @property
    def velocity(self) -> int: return self._velocity

    @property
    def ETRDY(self) -> int: return self._etrdy

    @property
    def cost(self) -> int: return self._cost

    @property
    def cover_area(self) -> CoverArea: return self._area

    @property
    def possibility(self) -> int: return self._poss

    def get_expected_percentage_of_water_by_min(self, minutes: int) -> float:
        """ Returns the estimated water percentage by time """
        if self._tank >= minutes:
            return 100
        else:
            return minutes / self._tank * 100

    def get_water_fill_time_by_current_percentage(self, percentage: float) -> float:
        """ Returns the estimated water filling (100%) time from the current water percentage """
        return int(self._tank * (1-0.01*percentage) * 10) / 10  # TODO: need to check it this work fine


class Aircrafts:
    """ Aircraft Information List """

    _aircraft_list = {key: BasicAircraft(val) for key, val in spec_sheet.items()}

    def __getitem__(self, key): return self._aircraft_list[key]

    @classmethod
    def get(cls, key, default=None): return cls._aircraft_list.get(key, default)

    @classmethod
    def get_by_aid(cls, key, default=None): return cls.get(key[:2], default)

    @classmethod
    def keys(cls): return cls._aircraft_list.keys()

    @staticmethod
    def to_json(): return _cached_json
