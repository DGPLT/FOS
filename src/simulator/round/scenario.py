# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : scenario.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ??????
Description : Game Scenarios (Rounds)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from math import log10

from operation import OperationOrderList
from ..unit.unit_table import UnitTable
from ..unit.aircraft import Aircraft
from ..unit.targets import Targets


class GameScenarios:
    """ Game Scenarios class that describes the game rounds """

    class Round:
        """ Game Data Holder class for each round """

        def __init__(self, round_num: int):
            self._round_num = round_num
            self._data = OperationOrderList()
            self._unit_table = UnitTable()
            self._used_money = 0
            self._time_lapse = 0

        @property
        def round_num(self):
            return self._round_num

        @property
        def order_list(self):
            return self._data

        @property
        def unit_table(self):
            return self._unit_table

        @property
        def score(self):
            #TODO: Adjust this calculation
            return self._time_lapse**2 + log10(self._used_money)

        def add_used_money(self, add: int):
            self._used_money += add

        def add_lapsed_time(self, add: int):
            self._time_lapse += add

    def __init__(self):
        self._current_round = 0
        self._rounds = {1: self.Round(1), 2: self.Round(2), 3: self.Round(3)}

    @property
    def current_round(self):
        return self._rounds[self._current_round]

    async def run_game(self, api, visualizer) -> bool:
        """ Run the game
        :return: False if the game is over, True otherwise
        """

        current_round = self.current_round
        unit_table = current_round.unit_table

        # Update timeline
        unit_table.update_table()

        # Check if 20 min lasts
        if unit_table.is_next_sequence():
            request, option, func = await api.resolve()

        

        #TODO: Proceed the game with the given request, option, and function
        return True

    async def start_new_round(self):
        """ Start a new round """
        self._current_round += 1


    #TODO: Create some caluculation methods for game scenarios
