# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : locations.py & Last Modded : 2023.05.18. ###
Coded with Python 3.10 Grammar by Kim, KyoungHun
Description : Target Information Maintainer Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from random import randrange, choice, sample
from enum import Enum
import json
import copy

from config.coordinates import coordinates as _coordinates


class TargetList:
    """ Target List contains Targets, Lakes and Bases """

    def __init__(self, round_num: int):
        self._coordinates = copy.deepcopy(_coordinates)
        self.targets = TargetList.Targets(self._coordinates, round_num)
        self.lakes = TargetList._Locations(self._coordinates, "Lakes")
        self.bases = TargetList._Locations(self._coordinates, "Bases")

    class _Locations:
        def __init__(self, coordinates, type_key: str):
            self._coordinates = coordinates
            self._TYPE = type_key
            self._data_holder = TargetList.Location
            self._cached = {}

        def __getitem__(self, key):
            data = self._coordinates[self._TYPE][key]
            if key in self._cached:
                return self._cached[key]
            return self._data_holder(data)

        def keys(self): return self._coordinates[self._TYPE].keys()

    class Targets(_Locations):
        """ Current Target Information List """

        @staticmethod
        def relation(key1: str, key2: str) -> int:
            """ Return Relation between key1 and key2 """
            _key1 = int(key1.removeprefix("T")) - 1
            _key2 = int(key2.removeprefix("T")) - 1
            return abs(_key1 % 3 - _key2 % 3) ** 2 + abs(_key1 % 3 - _key2 % 3) ** 2

        def __init__(self, coordinates, round_num: int):
            super().__init__(coordinates, "Targets")
            self._data_holder = TargetList.Target

            # Select Possible Fire Area & Select Target on Fire
            keys = sorted(list(self.keys()))
            if round_num == 1:
                target_type = {key: 0 for key in keys}
                target_threats = {key: 0 for key in keys}
                target_priorities = {key: 0 for key in keys}
                occurred = choice(keys)
                target_type[occurred] = 2
                target_threats[occurred] = 100
                target_priorities[occurred] = 1
            elif round_num == 2:
                opt = choice((0, 1, 3, 4))
                area = [keys[i] for i in (opt, opt+1, opt+3, opt+4)]
                occurred = sample(area, round_num)
                target_type = {key: 2 if key in occurred else 1 if area else 0 for key in keys}
                target_threats = {key: 100 if key in occurred else randrange(1, 100) if area else 0 for key in keys}
                target_priorities = {data[0]: i for i, data in enumerate(sorted(target_threats.items(), key=lambda x: x[1], reverse=True))}
            else:
                selected = sample(keys, round_num)
                target_type = {key: 2 if key in selected else 1 for key in keys}
                target_threats = {key: 100 if key in selected else randrange(1, 100) for key in keys}
                target_priorities = {data[0]: i for i, data in enumerate(sorted(target_threats.items(), key=lambda x: x[1], reverse=True))}

            [self[key].init_property(target_type[key], target_threats[key], target_priorities[key]) for key in keys]

        def mark_targeted(self, target_name):
            """ Mark Targeted to Target """
            self[target_name].set_targeted()

        def apply_targeting_operation(self, target_name: str, possibility_of_aircraft: int, still_targeted: bool) -> bool:
            """ Apply Targeting Operation - Check if fire is suppressed
            :return True: when fire is suppressed
            """
            target = self[target_name]
            result = False

            if target.type == self._data_holder.TargetType.NONE:
                result = True
            else:
                possibility = target.probability * possibility_of_aircraft / 100
                if randrange(0, 101) <= possibility:
                    target.set_suppressed()
                    result = True

            # Mark Not-Targeted/Still-Targeted
            target.set_targeted(still_targeted)

            return result

        def check_all_fires_suppressed(self) -> bool:
            """ Check All the fires are currently suppressed """
            return True not in [self[key].type == self._data_holder.TargetType.FIRE for key in self.keys()]

        def update_target_list(self):
            """ Update Target List at every order time
            **** PRIORITY IS NOT BEING UPDATED WITH THIS METHOD ****
            """
            keys = self.keys()

            # Decrease Probability of Suppressing Fire
            fires = [self[key] for key in keys if self[key].type == self._data_holder.TargetType.FIRE]
            [fire.set_probability(fire.probability-5) for fire in fires]  # decrease by 5

            # Check if fire is spreading to other targets
            possibles = [self[key] for key in keys if self[key].type == self._data_holder.TargetType.POSSIBLE]
            [tg.set_fire_occurred() for tg in possibles if randrange(0, 101) <= tg.threat and randrange(0, 20) == 0]

    class Location:
        """ Coordination Holder Class """
        def __init__(self, loc_dict):
            self._loc_dict = loc_dict

        @property
        def lat(self): return self._loc_dict["latitude"]

        @property
        def long(self): return self._loc_dict["longitude"]

        @property
        def coords(self) -> tuple[int, int]: return self._loc_dict["longitude"], self._loc_dict["latitude"]

    class Target(Location):
        """ Target Coordination Holder Class """

        class TargetType(Enum):
            NONE = 0
            POSSIBLE = 1
            FIRE = 2

        def init_property(self, target_type: int, threat: int, priority: int):
            self.set_property(target_type, abs(threat) if abs(threat) <= 100 else 100, priority, False,
                              100 if self.TargetType(target_type) == self.TargetType.FIRE else 0)

        def set_property(self, target_type: int, threat: int, priority: int, targeted: bool, probability: int):
            self._loc_dict["targeted"] = targeted
            self._loc_dict["priority"] = priority
            self._loc_dict["type"] = target_type
            self._loc_dict["threat"] = abs(threat) if abs(threat) <= 100 else 100
            self._loc_dict["probability"] = probability

        def set_targeted(self, targeted=True): self._loc_dict["targeted"] = targeted

        def set_suppressed(self):
            self.set_property(0, 0, 0, False, 0)

        def set_probability(self, probability):
            if probability < 0:
                probability = 0
            elif probability > 100:
                probability = 100
            self._loc_dict["probability"] = probability

        def set_fire_occurred(self):
            self._loc_dict["type"] = 2
            self._loc_dict["probability"] = 100

        @property
        def is_targeted(self): return self._loc_dict["targeted"]

        @property
        def priority(self): return self._loc_dict["priority"]

        @property
        def type(self): return self.TargetType(self._loc_dict["type"])

        @property
        def threat(self): return self._loc_dict["threat"]

        @property
        def probability(self): return self._loc_dict["probability"]

    def to_json(self): return json.dumps(self._coordinates)
