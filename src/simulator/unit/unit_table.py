# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : unit_table.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by DOO, JINSEO
Description : Unit Table Management Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from random import choice, randrange

from ..round.operation import OperationOrderList
MissionType = OperationOrderList.MissionType
from .locations import TargetList
from .aircraft import Aircrafts


class UnitTable(dict):
    """ UnitTable Management Class """

    _ORDER_SEQUENCE_INTERVAL = 20

    # Aircraft ID List
    _aircraft_ids = (k+"-"+i for i in ("A", "B") for k in Aircrafts.keys())

    @classmethod
    def get_aircraft_ids(cls):
        return cls._aircraft_ids

    @staticmethod
    def get_dist(l1: tuple[int, int], l2: tuple[int, int]) -> float:
        """ Get Distance between l1(x, y) and l2(x, y) """
        return ((l1[0]-l2[0])**2 + (l1[1]-l2[1])**2)**0.5

    @staticmethod
    def hour_to_min(time: str) -> int:
        return int(time[:2]) * 60 + int(time[2:])

    @staticmethod
    def time_adder(t1: str, t2: int) -> str:
        """ Add t2 (int) to t1 (str) """
        if int(t1[2:]) + t2 < 60:
            result = "0" + str(int(t1) + t2) if t1[0]=="0" else str(int(t1) + t2)
        else:
            if int(t1[1]) == 9:
                result = "10" + str(int(t1[2:]) + t2 - 60) if t1[0]=="0" else "20" + str(int(t1[2:]) + t2 - 60)
            else:
                result = "0" + str(int(t1[1])+1) + str(int(t1[2:]) + t2 - 60) if t1[0] == "0" else str(int(t1[:2])+1) + str(int(t1[2:]) + t2 - 60)

        # 2400 to 0000
        if t1[:2] == "24":
            return "0000"

        return result + "0" if len(result) == 3 else result

    def __init__(self, order_list: OperationOrderList, target_list: TargetList):
        super().__init__(self._gen_init_table())
        self._current_time: str = "0559"
        self._order_list: OperationOrderList = order_list
        self._target_list: TargetList = target_list
        self._base_list = list(target_list.bases.keys())
        self._order_mutex: bool = False

    def is_next_sequence(self) -> bool:
        """ Returns true if current time is 0600, 0620, 0640 etc """
        return int(self._current_time) % self._ORDER_SEQUENCE_INTERVAL == 0

    @property
    def current_time(self) -> str:
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

    def update_table(self):
        """ Update table for each minute """

        # One minute forward
        self._current_time = self.time_adder(self._current_time, 1)

        # Check if aircraft returned, update water tank
        self.update_state()

        # 현재 시간이랑 도착시간이랑 비교해서 도착을 했더라 => 불이 꺼졌는지 아닌지 확인 == 일때 확인
        ## 물탱크 0으로 만들기
        ## 모든 불 상태 확인



    def update_state(self):
        """ Check aircraft returned """

        for aid, aircraft in self.items():
            if aircraft['Ordered'] and int(aircraft['ETR']) <= int(self._current_time):
                # Reset Aircraft Status
                aircraft['Ordered'] = False
                aircraft['Available'] = True
                aircraft['ETR'] = ""
                aircraft['ETD'] = ""
                aircraft['ETA'] = ""
                aircraft['Current Water'] = 0

                # TODO: Set Done to Order List

            elif not aircraft['Ordered'] and aircraft['Current Water'] != 100:
                aircraft['Current Water'] += Aircrafts[aid[0:2]].get_expected_percentage_of_water_by_min(1)

    def calculate_position(self, l1, l2, start_time, velocity) -> tuple[int, int]:
        """ Return aircraft's position(x, y) calculated """

        h = self.get_dist(l1, l2)
        cos = (l2[0] - l1[0]) / h
        sin = (l2[1] - l1[1]) / h

        x_velocity = cos * velocity
        y_velocity = sin * velocity
        
        time_past = self.hour_to_min(self._current_time) - self.hour_to_min(start_time)

        return round(l1[0] + x_velocity * time_past), round(l1[1] + y_velocity * time_past)

    def get_current_positions(self) -> dict[str, tuple[int, int]]:
        """" Return the positions of the aircrafts on operation """

        positions: dict[str, tuple[int, int]] = {}

        for order in order_list:
            if order._done:
                continue

            if order._mission_type == 1:
                if int(current_time) < int(self[ETA]):
                    loc_from = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                    loc_to = self.get_coordinate("Targets", order._target)
                else:
                    l1 = self.get_coordinate("Targets", order._target)   
                    l2 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])           

            elif order._mission_type == 2:
                if int(current_time) < int(self[ETA]):
                    l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                    l2 = self.get_coordinate("Targets", order._target[:2])
                else:
                    l1 = self.get_coordinate("Targets", order._target[:2])   
                    l2 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])   

            elif order._mission_type == 3:
                if int(current_time) < int(self[ETA]):
                    # if current time < departure time + time to get to the lake
                    if int(current_time) < int(time_adder(self[ETD], (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) / Aircraft[order._aircraft_id[:2]].velocity))):
                        l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                        l2 = self.get_coordinate("Lakes", "L1")
                    else:
                        l1 = self.get_coordinate("Lakes", "L1")
                        l2 = self.get_coordinate("Targets", order._target)
                else:
                    l1 = self.get_coordinate("Targets", order._target)   
                    l2 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])                         

            elif order._mission_type == 4:
                if int(current_time) < int(self[ETA]):
                    # if current time < departure time + time to get to the lake
                    if int(current_time) < int(time_adder(self[ETD], (self.get_dist(self.get_coordinate("Bases", self[order._aircraft_id]['Base']), self.get_coordinate("Lakes", "L1")) / Aircraft[order._aircraft_id[:2]].velocity))):
                        l1 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])
                        l2 = self.get_coordinate("Lakes", "L1")
                    else:
                        l1 = self.get_coordinate("Lakes", "L1")
                        l2 = self.get_coordinate("Targets", order._target[:2])
                else:
                    l1 = self.get_coordinate("Targets", order._target[:2])
                    l2 = self.get_coordinate("Bases", self[order._aircraft_id]['Base'])

            positions[order._aircraft_id] = calculate_position(l1, l2, self[ETD], Aircraft[order._aircraft_id[:2]].velocity)

        return positions

    def apply_order(self, order_xml: str):
        """ Apply orders to the table """

        # Let OperationOrderList Add New Orders
        ## Check if the order time is correct
        self._order_list.add_order(order_xml, self._current_time, , )

        # Apply Details of new order to the table
        for order in self._order_list[-1]:
            this = self[order.aircraft_id]
            this['Ordered'] = True
            this['Available'] = False

            estimated_time_to_back = self.get_dist(self._target_list.bases[this['Base']]., self._target_list.targets[order.target[0]]) / Aircrafts[order.aircraft_id[0:2]].velocity
            if order.mission_type in (MissionType.FILL_DIRECT, MissionType.FILL_INDIRECT):  # lake, direct/indirect to target
                estimated_time_to_go = (self.get_dist(self.get_coordinate("Bases", this['Base']), self.get_coordinate("Lakes", "L1")) + self.get_dist(self.get_coordinate("Lakes", "L1"), self.get_coordinate("Targets", order._target))) / Aircraft[order._aircraft_id[0:2]].velocity
            else:  # no lake
                estimated_time_to_go = estimated_time_to_back

            # time1 : time to get to target, time2 : time to return from target
            self[order.aircraft_id]['ETD'] = self.time_adder(self._current_time, Aircrafts[order.aircraft_id[0:2]].ETRDY)
            self[order.aircraft_id]['ETA'] = self.time_adder(self[order.aircraft_id]['ETD'], time1)

            self[order.aircraft_id]['ETR'] = self.time_adder(self[order.aircraft_id]['ETA'], time2)

            # TODO: Update Target Status

    def _gen_init_table(self):
        """ Generate Initial Table """
        return {
            key: {
                "Ordered": False,
                "Available": True,
                "ETR": "",
                "ETD": "",
                "ETA": "",
                "Base": choice(self._base_list),
                "Current Water": randrange(0, 101)
            } for key in self.get_aircraft_ids()
        }
