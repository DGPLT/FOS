# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : operation.py & Last Modded : 2023.05.16. ###
Coded with Python 3.10 Grammar by Oh, Myoungjin
Description : Operation Order Related Classes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from __future__ import annotations

from typing import Callable
from enum import Enum
import xmltodict
import json

from ..unit.aircraft import BasicAircraft


class OperationOrderList(dict):
    """ Operation OrderList class """

    class MissionType(Enum):
        """ Mission Type Enum """
        DIRECT = 1
        INDIRECT = 2
        FILL_DIRECT = 3
        FILL_INDIRECT = 4

        def validate_target(self, target, aircraft_type: BasicAircraft.Type):
            """ Validate target
            :raise ValueError: When target is not a valid
            """
            # TODO: 확인해야 할 것:
            # TODO: 미션 타입 맞게 타겟 개수 들어왔고(1개 이거나 2개), 그 두 타겟간 비행체가 감당할 수 있는 거리가 맞는지

    class OperationOrder:
        """ Single Operation Order class """

        def __init__(self, order_id: int, ordered_time: str, base: str,
                     aircraft_type: str, aircraft_id: str, mission_type: str, course: str):
            self._order_id = order_id
            self._ordered_time = ordered_time
            self._base = base
            self._aircraft_type = aircraft_type
            self._aircraft_id = aircraft_id
            self._target = course.replace(" ", "").split(",")
            self._mission_type = OperationOrderList.MissionType(int(mission_type))
            self._done = False

        @property
        def order_id(self) -> int: return self._order_id

        @property
        def ordered_time(self) -> str: return self._ordered_time

        @property
        def base(self) -> str: return self._base

        @property
        def aircraft_type(self) -> str: return self._aircraft_type

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

        def validate_order(self, ids: tuple[tuple[str, str], ...], targets: tuple[str],
                           get_base: Callable[[str], str]) -> OperationOrderList.OperationOrder:
            """ Validate the order """
            # TODO: Validation for Aircraft type

            if self._aircraft_id not in ids:
                raise ValueError("Aircraft ID is not valid")

            if self._target not in targets:
                # TODO: 타겟 자료형 좀
                raise ValueError("Target Name is not valid")

            # TODO: 미션 타입

            if self._base != get_base(self._aircraft_id):
                raise ValueError(f"Cannot find an aircraft [{self._aircraft_id}] located on base [{self._base}]")

            # TODO: Validate more
            return self

        @staticmethod
        def load_orders(order_xml: str, oid: int, current_time: str, get_base: Callable[[str], str],
                        aircrafts: tuple[tuple[str, str], ...], targets: tuple[str]
                        ) -> tuple[OperationOrderList.OperationOrder, ...]:
            """ Load xml orders
            :raise KeyError: if key of each order is not valid
            :raise ValueError: if some values are not valid
            """

            # Parse XML
            xml_parse = xmltodict.parse(order_xml)
            xml_dict = json.loads(json.dumps(xml_parse))
            time_line = xml_dict["operations"].pop("time")
            order_list = xml_dict["operations"].pop("order")

            # Check XML Schema
            if len(xml_dict) != 1 or len(xml_dict["operations"]) > 0:
                raise KeyError("Too many keys exist in the XML then expected.")

            # Check Timeline
            if time_line != current_time:
                raise ValueError("Invalid time line: Does not match to current time.")

            return tuple(OperationOrderList.OperationOrder(oid, current_time, **order)
                         .validate_order(aircrafts, targets, get_base) for order in order_list)

    def add_order(self, order_xml: str, current_time: str, get_base: Callable[[str], str],
                  aircrafts: tuple[tuple[str, str], ...], targets: tuple[str]):
        """ Add an order to the order list """
        self[len(self)+1] = self.OperationOrder.load_orders(
            order_xml, len(self)+1, current_time, get_base, aircrafts, targets)
