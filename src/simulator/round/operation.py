# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : operation.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ??????
Description : Operation Order Related Classes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import xml.etree.ElementTree as elemTree


class OperationOrderList(dict):
    """ Operation OrderList class """

    class OperationOrder:
        """ Single Operation Order class """
        def __init__(self, order_id: int, aircraft_id: str, mission_type: int, target: str):
            self._order_id = order_id
            self._aircraft_id = aircraft_id
            self._mission_type = mission_type
            self._target = str
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
        def mission_type(self) -> int:
            """ Return mission type """
            return self._mission_type

        @property
        def is_finished(self) -> bool:
            """ Return true if the order is finished """
            return self._done

        def finish_order(self):
            """ Finish the order """
            self._done = True

        def validate_orders(self):
            """ Validate the order """
            #TODO
            pass

        def load_orders(self, order_xml: str) -> (OperationOrder, ...):
            """ Load xml orders """
            #TODO
            pass

    def add_order(self, order_xml: str):
        """ Add an order to the order list """
        self[len(self)+1] = self.OperationOrder.load_orders(order_xml)

