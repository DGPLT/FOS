# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : unit_table.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by DOO, JINSEO
Description : Unit Table Management Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from random import choice, randrange

from aircraft import Aircraft
from config.coordinates import coordinates


class UnitTable(dict):
    """ UnitTable Management Class """

    # Base Location Selector
    _base_list = coordinates["Bases"].keys()

    @classmethod
    def get_aircraft_ids(cls):
        TODO:return (k for k in range  for i in Aircraft.keys())

    @classmethod
    def select_base(cls) -> str:
        return choice(cls._base_list)

    @staticmethod
    def get_dist(l1, l2) -> float:
        """ Get Distance between l1 and l2 """
        return ((l1[0]-l1[1])**2 + (l2[0]-l2[1])**2)**0.5

    @staticmethod
    def time_adder(t1: str, t2: int) -> str:
        """ Add t2 (omt) to t1 (str) """
        if int(t1[2:]) + t2 < 60:
            return str(int(t1) + t2)
        else:
            if int(t1[1]) == 9:
                return "10" + str(int(t1[2:]) + t2 - 60)
            else:
                return "0" + str(int(t1[1])+1) + str(int(t1[2:]) + t2 - 60)

    def __init__(self):
        super().__init__(self._gen_init_table())
        self._current_time: str = "0600"

    @property
    def current_time(self):
        return self._current_time

    def __setitem__(self, key, val):
        raise NotImplementedError("This dictionary cannot be updated")

    def __delitem__(self, key):
        raise NotImplementedError("This dictionary does not allow delete")


    def is_now(self, order):
        return order["order_id"] == self.order_num

    def get_coordinate(self, typeof_point, point):
        x = coordinates[typeof_point][point]["Latitude"]
        y = coordinates[typeof_point][point]["Longtitude"]

        return (x, y)

    # update table when order made
    def update_table(self, data, order_number):

        self.time = self.time_adder(self.time, 20)

        operation = filter(self.is_now(order_number), data)

        for order in operation:
            self.table[order._aircraft_id]['Ordered'] = True
            self.table[order._aircraft_id]['Available'] = False

            # direct to target
            if order._mission_type == 1:
                time1 = self.get_dist(self.get_coordinate("Bases", self.table[order._aircraft_id]['Base']), self.get_coordinate("Targets", order._target)) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
                time2 = time1
            
            # indirect to target
            elif order._mission_type == 2:
                time1 = self.get_dist(self.get_coordinate("Bases", self.table[order._aircraft_id]['Base']), self.get_coordinate("Targets", order._target[0:2])) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
                time2 = time1

            # lake, direct to target 
            elif order._mission_type == 3:
                time1 = (self.get_dist(self.get_coordinate("Bases", self.table[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) + self.get_dist(self.get_coordinate("Lakes", "L1"), self.get_coordinate("Targets", order._target))) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
                time2 = self.get_dist(self.get_coordinate("Targets", order._target), self.get_coordinate("Bases", self.table[order._aircraft_id]['Base'])) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
            
            # lake, indirect to target
            elif order._mission_type == 4:
                time1 = (self.get_dist(self.get_coordinate("Bases", self.table[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) + self.get_dist(self.get_coordinate("Lakes", "L1"), self.get_coordinate("Targets", order._target[0:2]))) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
                time2 = self.get_dist(self.get_coordinate("Targets", order._target[0:2]), self.get_coordinate("Bases", self.table[order._aircraft_id]['Base'])) / spec_sheet[order._aircraft_id[0:2]]['Velocity']
            
            
            # time1 : time to get to target, time2 : time to return from target
            self.table[order._aircraft_id]['ETD'] = self.time_adder(self.time, spec_sheet[order._aircraft_id[0:2]]['ETRDY'])
            self.table[order._aircraft_id]['ETA'] = self.time_adder(self.table[order._aircraft_id]['ETD'], time1)

            self.table[order._aircraft_id]['ETR'] = self.time_adder(self.table[order._aircraft_id]['ETA'], time2)

    # Check if a aircraft returned
    def update_state(self, time: int):

        self.time = self.time_adder(self.time, time)
        for aircraft in self.table:
            if aircraft['Ordered'] and aircraft['ETR'] <= int(self.time):
                aircraft['Ordered'] = False
                aircraft['Available'] = True
                aircraft['ETR'] = None
                aircraft['ETD'] = None
                aircraft['ETA'] = None
                aircraft['Curren Water'] = 0

    def _gen_init_table(self):
        """ Generate Initial Table """
        ids = iter(self.get_aircraft_ids())
        return {
            next(ids): {
                "Ordered": False,
                "Available": True,
                "ETR": None,
                "ETD": None,
                "ETA": None,
                "Base": self.select_base(),
                "Current Water": randrange(0, 101)
            } for i in range(0, 31)
        }

