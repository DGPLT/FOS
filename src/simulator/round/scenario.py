# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : scenario.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ??????
Description : Game Scenarios (Rounds)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
            self._score = 0

    def __init__(self):
        self._current_round = 0
        self._rounds = {1: self.Round(1), 2: self.Round(2), 3: self.Round(3)}

    async def run_game(self, api, visualizer) -> bool:
        """ Run the game
        :return: False if the game is over, True otherwise
        """

        request, option, func = await api.resolve()

        #TODO: Proceed the game with the given request, option, and function
        return True

    async def start_new_round(self):
        """ Start a new round """
        self._current_round += 1


    #TODO: Create some caluculation methods for game scenarios
