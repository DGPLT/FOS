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
get_by_aid = Aircrafts.get_by_aid


class UnitTable(dict):
    """ UnitTable Management Class """

    # Aircraft ID List
    _aircraft_ids = tuple(k+"-"+i for i in ("A", "B") for k in Aircrafts.keys())

    @classmethod
    def get_aircraft_ids(cls) -> tuple[str, ...]:
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
            result = "0" + str(int(t1) + t2) if t1[0] == "0" else str(int(t1) + t2)
        else:
            if int(t1[1]) == 9:
                result = "10" + str(int(t1[2:]) + t2 - 60) if t1[0] == "0" else "20" + str(int(t1[2:]) + t2 - 60)
            else:
                result = "0" + str(int(t1[1])+1) + str(int(t1[2:]) + t2 - 60) if t1[0] == "0" \
                    else str(int(t1[:2])+1) + str(int(t1[2:]) + t2 - 60)

        ''' Disable Time Conversion
        # 2400 to 0000
        if int(result[:2]) >= 24:
            return f"{int(result[:2])-24}" + result[2:]
        '''

        #TODO: Test Required

        return result + "0" if len(result) == 3 else result

    def __init__(self, order_list: OperationOrderList, target_list: TargetList):
        self._current_time: str = "0559"
        self._order_list: OperationOrderList = order_list
        self._target_list: TargetList = target_list
        self._base_list = list(target_list.bases.keys())
        self._order_mutex: bool = False
        super().__init__(self._gen_init_table())

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

    def update_table(self) -> tuple[int, bool]:
        """ Update table for each minute
        :return tuple[int, bool]: (used money, file_suppressed)
        """
        targets = self._target_list.targets

        # One minute forward
        self._current_time = self.time_adder(self._current_time, 1)

        # Update TargetList
        ## Fire might be spread after this method is called
        targets.update_target_list()

        # Update Aircraft Status
        ## if aircraft returned, update water tank
        used_money = self.update_state()

        return used_money, targets.check_all_fires_suppressed()  # Check if all fires are suppressed

    def update_state(self) -> int:
        """ Update Aircraft Status - Increase Water Tank Level only for not Ordered Aircrafts
        :return int: used money
        """
        targets = self._target_list.targets
        order_list = self._order_list
        used_money = 0

        for aid, aircraft in self.items():
            order = order_list.get(aid, None)
            # Ordered Aircraft =========================================================================================
            if aircraft['Ordered']:  # 'Ordered' means that current_time is after operation_time
                ## Check Departure -------------------------------------------------------------------------------------
                if aircraft['Available']:  # If an aircraft is available, then it means the aircraft is not departed
                    if int(aircraft['ETD']) <= int(self._current_time):
                        ### Set the aircraft not available
                        aircraft['Available'] = False
                        ### Raise the amount of money spent
                        used_money += get_by_aid(aid).cost
                ## Check Arrival ---------------------------------------------------------------------------------------
                elif int(aircraft['ETA']) == int(self._current_time):
                    ### Check if the fire is suppressed
                    targets.apply_targeting_operation(
                        order.target[-1], aircraft['Current Water'] * get_by_aid(aid).possibility / 100)
                    ### Set Water Level 0
                    aircraft['Current Water'] = 0
                ## Check Return ----------------------------------------------------------------------------------------
                elif int(aircraft['ETR']) <= int(self._current_time):
                    ### Reset Aircraft Status
                    aircraft['Ordered'] = False
                    aircraft['Available'] = True
                    aircraft['ETR'] = ""
                    aircraft['ETD'] = ""
                    aircraft['ETA'] = ""
                    aircraft['Current Water'] = 0
                    ### Set Done to Order List
                    order.finish_order()
            # Not Ordered & Check Operation Time =======================================================================
            elif order and not order.is_finished and int(order.operation_time) <= int(self._current_time):
                aircraft['Ordered'] = True  # Mark Ordered
            # Not Ordered & Not Full Water Tank ========================================================================
            elif aircraft['Current Water'] < 100:
                aircraft['Current Water'] += get_by_aid(aid).get_expected_percentage_of_water_by_min(1)
                if aircraft['Current Water'] > 100:
                    aircraft['Current Water'] = 100

        return used_money

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
        """" Return the positions of the aircraft on operation """

        positions: dict[str, tuple[int, int]] = {}
        targets = self._target_list.targets
        lakes = self._target_list.lakes
        bases = self._target_list.bases
        order_list = self._order_list

        for aid, this in filter(lambda x: not x[1]['Available'], self.items()):
            order = order_list[aid]
            if order.mission_type in (MissionType.DIRECT, MissionType.INDIRECT):
                if int(self._current_time) < int(this['ETA']):
                    loc_from = bases[this['Base']]
                    loc_to = targets[order.target[0]]
                else:
                    loc_from = targets[order.target[0]]
                    loc_to = bases[this['Base']]
            else:
                if int(self._current_time) < int(this['ETA']):
                    # if current time < departure time + time to get to the lake
                    if int(self._current_time) < int(self.time_adder(this['ETD'], round(self.get_dist(
                            bases[this['Base']].coords, lakes['L1'].coords) / get_by_aid(aid).velocity))):
                        loc_from = bases[this['Base']]
                        loc_to = lakes['L1']
                    else:
                        loc_from = lakes['L1']
                        loc_to = targets[order.target[0]]
                else:
                    loc_from = targets[order.target[0]]
                    loc_to = bases[this['Base']]

            positions[aid] = self.calculate_position(loc_from.coords, loc_to.coords, this['ETD'], get_by_aid(aid).velocity)

        return positions

    def apply_order(self, order_xml: str):
        """ Apply orders to the table """
        targets = self._target_list.targets
        lakes = self._target_list.lakes
        bases = self._target_list.bases

        # Let OperationOrderList Add New Orders
        ## Check if the order time is correct
        self._order_list.add_order(
            order_xml, self._current_time, get_by_aid, self._aircraft_ids, lambda aid: self[aid], targets.keys())

        # Initialize Targeted Values
        [targets[key].set_targeted(False) for key in targets.keys()]

        # Apply Details of new order to the table
        ## Only iterate for ongoing orders
        for order in filter(lambda x: not x.is_finished, self._order_list.values()):
            this = self[order.aircraft_id]
            model = get_by_aid(order.aircraft_id)

            estimated_time_to_back = self.get_dist(bases[this['Base']].coords, targets[order.target[0]].coords) / model.velocity
            if order.mission_type in (MissionType.FILL_DIRECT, MissionType.FILL_INDIRECT):  # lake, direct/indirect to target
                estimated_time_to_go = (self.get_dist(bases[this['Base'].coords], lakes[this['L1']].coords)
                                        + self.get_dist(lakes[this['L1']].coords, targets[order.target[0]].coords)) / model.velocity
            else:  # no lake
                estimated_time_to_go = estimated_time_to_back

            # time1 : time to get to target, time2 : time to return from target
            this['ETD'] = self.time_adder(order.operation_time, round(model.ETRDY))
            this['ETA'] = self.time_adder(this['ETD'], round(estimated_time_to_go))
            this['ETR'] = self.time_adder(this['ETA'], round(estimated_time_to_back))

            # Update Target Status (Targeted)
            targets[order.target[-1]].set_targeted()

    def _gen_init_table(self):
        """ Generate Initial Table """
        return {
            key: {
                'Ordered': False,
                'Available': True,
                'ETR': "",
                'ETD': "",
                'ETA': "",
                'Base': choice(self._base_list),
                'Current Water': randrange(0, 101)
            } for key in self.get_aircraft_ids()
        }
