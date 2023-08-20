# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : operation.py & Last Modded : 2023.07.08. ###
Coded with Python 3.10 Grammar by Jin, Hojin
Description : Operation Order Related Classes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from __future__ import annotations

from typing import Callable
from enum import Enum
import xmltodict
import json

from ..unit.aircraft import BasicAircraft
from ..unit.locations import TargetList
t_relation = TargetList.Targets.relation


class OperationOrderList(dict):
    """ Operation OrderList class """

    class MissionType(Enum):
        """ Mission Type Enum """
        DIRECT = 1
        INDIRECT = 2
        FILL_DIRECT = 3
        FILL_INDIRECT = 4

        def validate_target(self, aircraft_id: str, target: list, cover_area: BasicAircraft.CoverArea):
            """ Validate target
            :raise ValueError: When target is not a valid (Target Name Check is not supported)
            """
            if self == self.INDIRECT or self == self.FILL_INDIRECT:  # check the number of targets
                try:
                    required_cover_area = BasicAircraft.CoverArea(t_relation(*target))
                    if required_cover_area.value > cover_area.value:
                        raise ValueError
                except ValueError:  # if error occurred, then it means the distance between two targets is too large.
                    raise ValueError(f"Listed Targets are not available for this aircraft {aircraft_id}. (Too Far)")
            else:
                if len(target) != 1:
                    raise ValueError(f"Target must be specified for this aircraft {aircraft_id}.")

    class OperationOrder:
        """ Single Operation Order class """

        def __init__(self, time: str, base: str, aircraft_type: str, track_number: str, mission_type: str, course: str):
            self._operation_time = time  # operation start time
            self._base = base
            self._aircraft_type: BasicAircraft.Type = BasicAircraft.Type(aircraft_type)
            self._aircraft_id = track_number
            self._target = course.replace(" ", "").split(",")
            self._mission_type = OperationOrderList.MissionType(int(mission_type))
            self._done = False

        @property
        def operation_time(self) -> str: return self._operation_time

        @property
        def base(self) -> str: return self._base

        @property
        def aircraft_type(self) -> BasicAircraft.Type: return self._aircraft_type

        @property
        def aircraft_id(self) -> str: return self._aircraft_id

        @property
        def mission_type(self) -> OperationOrderList.MissionType: return self._mission_type

        @property
        def target(self) -> list[str]: return self._target

        @property
        def is_finished(self) -> bool:
            """ Return true if the order is finished """
            return self._done

        def finish_order(self):
            """ Finish the order """
            self._done = True

        def validate_order(self, current_time: str, get_by_aid: Callable[[str], BasicAircraft],
                           aid_list: tuple[str, ...], get_unit: Callable[[str], dict], targets: tuple[str, ...]
                           ) -> OperationOrderList.OperationOrder:
            """ Validate the order """

            # Check Timeline
            if self._operation_time <= current_time:  # Check if the timeline is equal to or earlier than the current one
                raise ValueError(f"Invalid time line: Unable to create an order for past time."
                                 f" ({self._operation_time} <= {current_time}, {self._aircraft_id})"
                                 f" Make sure that the time line is set to future.")

            # Check Aircraft ID Validity
            if self._aircraft_id not in aid_list:
                raise ValueError(f"Aircraft ID: {self._aircraft_id} is not valid")

            aircraft_model = get_by_aid(self._aircraft_id)
            aircraft_unit = get_unit(self._aircraft_id)

            # Check Unit Table Validity
            if self._base != aircraft_unit['Base']:
                raise ValueError(f"Cannot find an aircraft [{self._aircraft_id}] located on base [{self._base}]")

            # Check Aircraft Type Validity
            if self._aircraft_type != aircraft_model.type:
                raise ValueError(f"None of the registered {self._aircraft_type} named as {self._aircraft_id}.")

            # Check Target & Mission Type Value
            for tg in self._target:
                if tg not in targets:
                    raise ValueError(f"Target Name [{tg}] is not valid for this aircraft {self._aircraft_id}.")
            self._mission_type.validate_target(self._aircraft_id, self._target, aircraft_model.cover_area)

            # Check Validation between Aircraft Type and Mission Type
            ## Drone can be ordered with MissionType.DIRECT
            if self._aircraft_type == self._aircraft_type.Drone and self._mission_type != self._mission_type.DIRECT:
                raise ValueError(f"Drone {self._aircraft_id} is not available for mission type {self._mission_type}.")

            # Check Assigned Aircraft Availability
            if not aircraft_unit['Available']:
                raise ValueError(f"Aircraft {self._aircraft_id} is not available at this time. (Already Deployed)")

            return self

        @staticmethod
        def load_orders(order_xml: str, current_time: str, get_by_aid: Callable[[str], BasicAircraft],
                        aid_list: tuple[str, ...], get_unit: Callable[[str], dict], targets: tuple[str, ...]
                        ) -> dict[str: OperationOrderList.OperationOrder, ...]:
            """ Load xml orders
            :raise KeyError: if key of each order is not valid
            :raise ValueError: if some values are not valid
            """

            # Parse XML
            xml_parse = xmltodict.parse(order_xml)
            xml_dict = json.loads(json.dumps(xml_parse))
            operations = {} if xml_dict['operations'] is None else xml_dict['operations']
            order_list = operations.pop("order", [])
            if type(order_list) == dict:
                order_list = [order_list]

            # Check XML Schema
            if len(xml_dict) != 1 or len(operations) > 0:
                raise KeyError("Too many keys exist in the XML then expected.")

            return {order['track_number']: OperationOrderList.OperationOrder(**order).validate_order(
                current_time, get_by_aid, aid_list, get_unit, targets) for order in order_list}

    def add_order(self, order_xml: str, current_time: str, get_by_aid: Callable[[str], BasicAircraft],
                  aid_list: tuple[str, ...], get_unit: Callable[[str], dict], targets: tuple[str, ...]):
        """ Add an order to the order list or overwrite existing order with the same time and aircraft """
        self.update(self.OperationOrder.load_orders(order_xml, current_time, get_by_aid, aid_list, get_unit, targets))
