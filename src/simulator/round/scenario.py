# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : scenario.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ??????
Description : Game Scenarios (Rounds)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from math import log10
import traceback
import asyncio
import json

from .operation import OperationOrderList
from ..unit.unit_table import UnitTable
from ..unit.locations import TargetList
from ..unit.aircraft import Aircrafts


class GameScenarios:
    """ Game Scenarios class that describes the game rounds """

    _MAX_ROUND = 3

    class Round:
        """ Game Data Holder class for each round """

        def __init__(self, round_num: int):
            self._round_num = round_num
            self._data = OperationOrderList()
            self._target_list = TargetList(round_num)
            self._unit_table = UnitTable(self._data, self._target_list)
            self._used_money = 0
            self._time_lapse = 0
            self._win = False

        @property
        def round_num(self): return self._round_num

        @property
        def order_list(self): return self._data

        @property
        def unit_table(self): return self._unit_table

        @property
        def target_list(self): return self._target_list

        @property
        def score(self) -> int:
            #TODO: Adjust this calculation
            return int(((self._used_money/90.0)**1.16 + 10*log10((self._time_lapse+2)**2)) * 100)

        @property
        def is_win(self): return self._win

        def add_used_money(self, add: int): self._used_money += add

        def add_lapsed_time(self, add: int): self._time_lapse += add

        def set_win(self): self._win = True

    def __init__(self):
        self._current_round = 0
        self._rounds = {i: self.Round(i) for i in range(1, self._MAX_ROUND+1)}

    @property
    def current_round(self) -> Round:
        return self._rounds[self._current_round]

    async def run_game(self, api, visualizer) -> bool:
        """ Run the game
        :return: False if the game is over, True otherwise
        """

        current_round = self.current_round
        unit_table = current_round.unit_table

        # Update timeline
        if not unit_table.check_table_mutex():
            money_usage, suppressed = unit_table.update_table()  # updates are applied first

            ## Round Information Update
            current_round.add_used_money(money_usage)
            current_round.add_lapsed_time(1)

            ## Apply changes to Screen
            positions = unit_table.get_current_positions()
            await visualizer.apply_dataset(current_round.target_list, unit_table, positions)

            ## Check Target Safety
            if suppressed:
                current_round.set_win()
                return False  # Win!
            ## Check if time is over 2359 hrs
            elif unit_table.current_time > "2359" or unit_table.current_time == "0000":
                return False  # Game over
            ## Normal Operation
            else:
                unit_table.lock_table()  # Table lock

        request, option, func = await api.resolve()

        # If got operation order from controller
        if request == "/order":
            try:
                unit_table.apply_order(option)
                # If order successfully added
                await func(code=200, message="Success")
                await visualizer.add_order_log(option, unit_table.current_time)
                unit_table.release_table()  # Table release
            except Exception as e:
                traceback.print_exc()
                await func(code=500, message=repr(e))
        elif request == "/data":
            await func(spec_sheet=Aircrafts.to_json(),
                       target_list=lambda: current_round.target_list.to_json(),
                       unit_table=lambda: json.dumps(unit_table),
                       time=unit_table.current_time)
        else:
            await func(code=403)

        return True

    async def start_new_round(self, api, visualizer):
        """ Start a new round """
        self._current_round += 1
        if self._current_round > self._MAX_ROUND:
            raise ValueError("Round Number is out of range.")

        cur_round = self.current_round
        await visualizer.set_round_mode(cur_round.round_num, cur_round.unit_table, cur_round.target_list)

        # Wait until game start request is received
        while True:
            request, option, func = await api.resolve()
            if request == "/start":
                await func(round=self._current_round)
                break
            else:
                await func(code=401)
            await asyncio.sleep(0)

    async def end_this_round(self, api, visualizer) -> bool:
        """ End this round
        :return True: When player is win this round
        """
        cur_round = self.current_round
        # Show Result Panel
        await visualizer.show_score_panel(cur_round.round_num, cur_round.is_win, cur_round.score)
        while True:
            request, option, func = await api.resolve()
            if request == "/result":
                await func(round=cur_round.round_num, is_win=cur_round.is_win, score=cur_round.score)
                break
            else:
                await func(code=401)
            await asyncio.sleep(0)

        return cur_round.is_win and cur_round.round_num < 3
