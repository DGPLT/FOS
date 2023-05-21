# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : operation.py & Last Modded : 2023.05.16. ###
Coded with Python 3.10 Grammar by Oh, Myoungjin
Description : Operation Order Related Classes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from __future__ import annotations

from enum import Enum
import xmltodict
import json

from ..unit.unit_table import UnitTable
from ..unit.locations import TargetList


class OperationOrderList(dict):
    """ Operation OrderList class """

    class MissionType(Enum):
        """ Mission Type Enum """
        DIRECT = 1
        INDIRECT = 2
        FILL_DIRECT = 3
        FILL_INDIRECT = 4

    class OperationOrder:
        """ Single Operation Order class """

        def __init__(self, order_id: int, aircraft_id: str, mission_type: OperationOrderList.MissionType, target: str):
            self._order_id = order_id
            self._aircraft_id = aircraft_id
            self._mission_type = mission_type
            self._target = target
            self._done = False

        @property
        def order_id(self) -> int:
            """ Return order id """
            return self._order_id

        @property
        def aircraft_id(self) -> str:
            """ Return aircraft id """
            return self._aircraft_id

        @property
        def mission_type(self) -> OperationOrderList.MissionType:
            """ Return mission type """
            return self._mission_type

        @property
        def is_finished(self) -> bool:
            """ Return true if the order is finished """
            return self._done

        def finish_order(self):
            """ Finish the order """
            self._done = True

        def validate_orders(self) -> bool:
            """ Validate the order """
            assert self._aircraft_id in UnitTable.get_aircraft_ids(), 'Aircraft ID is not valid'
            assert self._target in TargetList.items(), 'Target is not valid'

            # TODO

        @staticmethod
        def load_orders(order_xml: str) -> tuple[OperationOrderList.OperationOrder, ...]:
            """ Load xml orders """
            xml_parse = xmltodict.parse(order_xml)
            xml_dict = json.loads(json.dumps(xml_parse))["operations"]
            if xml_dict["time"] == UnitTable.
            return ()

    def add_order(self, order_xml: str):
        """ Add an order to the order list """
        self[len(self)+1] = self.OperationOrder.load_orders(order_xml)
