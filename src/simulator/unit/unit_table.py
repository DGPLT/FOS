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
        return (k+"-"+i for k, i in map(Aircraft.keys(), ("A", "B")))

    @classmethod
    def select_base(cls) -> str:
        return choice(cls._base_list)

    @staticmethod
    def get_dist(l1, l2) -> float:
        """ Get Distance between l1 and l2 """
        return ((l1[0]-l2[0])**2 + (l1[1]-l2[1])**2)**0.5

    @staticmethod
    def time_adder(t1: str, t2: int) -> str:
        """ Add t2 (omt) to t1 (str) """
        if int(t1[2:]) + t2 < 60:
            result = "0" + str(int(t1) + t2) if t1[0]=="0" else str(int(t1) + t2)
        else:
            if int(t1[1]) == 9:
                result = "10" + str(int(t1[2:]) + t2 - 60) if t1[0]=="0" else "20" + str(int(t1[2:]) + t2 - 60)
            else:
                result = "0" + str(int(t1[1])+1) + str(int(t1[2:]) + t2 - 60) if t1[0] == "0" else str(int(t1[:2])+1) + str(int(t1[2:]) + t2 - 60)

        if t1[:2] == "24":
            return "0000"

        return result + "0" if len(result) == 3 else result
        #TODO: Check if fine with t1=2359 t2=1


    def __init__(self):
        super().__init__(self._gen_init_table())
        self._current_time: str = "0559"
        self._order_mutex: bool = False

    def is_next_sequence(self) -> bool:
        return #TODO: return true if "0600", "0620", "0640", etcs

    @property
    def current_time(self):
        return self._current_time

    def check_table_mutex(self) -> bool:
        """ Returns Table Lock Mutex status """
        return self._order_mutex

    def lock_table(self):
        """ Lock table until the operation order is conducted """
        self._order_mutex = True

    def release_table(self):
        """ Release table when the operation order is conducted """
        self._order_mutex = False

    def __setitem__(self, key, val):
        raise NotImplementedError("This dictionary cannot be updated")

    def __delitem__(self, key):
        raise NotImplementedError("This dictionary does not allow delete")


    def is_now(self, order):
        return order["order_id"] == self.order_num

    def get_coordinate(self, typeof_point, point):
        return coordinates[typeof_point][point].values

    def update_table(self):
        """ Update table for each minute """

        # One minute forward
        self._current_time = self.time_adder(self._current_time, 1)

        # Check if aircraft returned, update water tank
        self.update_state()

        # Apply order every 20 mins
        if int(_current_time[2:]) % 20 == 0:
            self.apply_order()


    def apply_order(self, order_list, order_number):
        """ Apply orders to the table """

        operation = filter(self.is_now(order_number), order_list)

        for order in operation:
            self[order._aircraft_id]['Ordered'] = True
            self[order._aircraft_id]['Available'] = False

            # direct to target
            if order._mission_type == 1:
                time1 = self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Targets", order._target)) / Aircraft[order._aircraft_id[0:2]].velocity
                time2 = time1
            
            # indirect to target
            elif order._mission_type == 2:
                time1 = self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Targets", order._target[0:2])) / Aircraft[order._aircraft_id[0:2]].velocity
                time2 = time1

            # lake, direct to target 
            elif order._mission_type == 3:
                time1 = (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) + self.get_dist(self.get_coordinate("Lakes", "L1"), self.get_coordinate("Targets", order._target))) / Aircraft[order._aircraft_id[0:2]].velocity
                time2 = self.get_dist(self.get_coordinate("Targets", order._target), self.get_coordinate("Bases", self[order._aircraft_id]['Base'])) / Aircraft[order._aircraft_id[0:2]].velocity
            
            # lake, indirect to target
            elif order._mission_type == 4:
                time1 = (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) + self.get_dist(self.get_coordinate("Lakes", "L1"), self.get_coordinate("Targets", order._target[0:2]))) / Aircraft[order._aircraft_id[0:2]].velocity
                time2 = self.get_dist(self.get_coordinate("Targets", order._target[0:2]), self.get_coordinate("Bases", self[order._aircraft_id]['Base'])) / Aircraft[order._aircraft_id[0:2]].velocity
            
            
            # time1 : time to get to target, time2 : time to return from target
            self[order._aircraft_id]['ETD'] = self.time_adder(self.time, Aircraft[order._aircraft_id[0:2]].ETRDY)
            self[order._aircraft_id]['ETA'] = self.time_adder(self[order._aircraft_id]['ETD'], time1)

            self[order._aircraft_id]['ETR'] = self.time_adder(self[order._aircraft_id]['ETA'], time2)

    def update_state(self):
        """ Check aircraft returned """

        for aircraft in self:
            if aircraft['Ordered'] and int(Aircraft['ETR']) <= int(self._current_time):
                aircraft['Ordered'] = False
                aircraft['Available'] = True
                aircraft['ETR'] = None
                aircraft['ETD'] = None
                aircraft['ETA'] = None
                aircraft['Current Water'] = 0
            elif not aircraft['Ordered']
                aircraft['Current Water'] += get_expected_percentage_of_water_by_min(1)

    def hour_to_min(time: str) -> int:
        return int(time[:2]) * 60 + int(time[2:])

    def calculate_position(self, l1, l2, start_time, velocity):
        """" Return aircraft's position caculated """

        h = get_dist(l1, l2)
        cos = (l2[0] - l1[0]) / h
        sin = (l2[1] - l1[1]) / h

        x_velocity = cos * velocity
        y_velocity = sin * velocity 
        
        time_past = self.hour_to_min(_current_time) - self.hour_to_min(start_time)

        return (l1[0] + x_velocity * time_past, l1[1] + y_velocity * time_past)

    def get_positions(self, order_list):
        """" Return the positions of the aircrafts on operation """

        positions = {}
        
        for order in order_list:
            if order._done:
                continue

            if order._mission_type == 1:
                l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                l2 = self.get_coordinate("Targets", order._target)

            elif order._mission_type == 2:
                l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                l2 = self.get_coordinate("Targets", order._target[:2])

            elif order._mission_type == 3:
                # if current time < departure time + time to get to the lake
                if int(current_time) < int(time_adder(self[ETD], (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) / Aircraft[order._aircraft_id[:2]].velocity))):
                    l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                    l2 = self.get_coordinate("Lakes", "L1")
                else:
                    l1 = self.get_coordinate("Lakes", "L1")
                    l2 = self.get_coordinate("Targets", order._target)

            else order._mission_type == 4:
                # if current time < departure time + time to get to the lake
                if int(current_time) < int(time_adder(self[ETD], (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) / Aircraft[order._aircraft_id[:2]].velocity))):
                    l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                    l2 = self.get_coordinate("Lakes", "L1")
                else:
                    l1 = self.get_coordinate("Lakes", "L1")
                    l2 = self.get_coordinate("Targets", order._target[:2])            

            positions[order._aircraft_id] = calculate_position(l1, l2, self[ETD], Aircraft[order._aircraft_id[:2]].velocity)
        
        return positions

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

