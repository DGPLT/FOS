# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Myung, Gyung Min
Description : Web Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from src.simulator.display.components import GameVisualizer

import json
import asyncio


class JSVisualizer(GameVisualizer):
    _PIXEL_EXPANSION = 2.3
    _MAX_CORDINATION = 300
    _SCREEN_WIDTH = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_HEIGHT = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_SIZE = (_SCREEN_WIDTH, _SCREEN_HEIGHT)

    visualize = True

    def __init__(self, logging: bool = True):
        super().__init__(logging)


    def is_pause_pressed(self) -> bool:
        """ Check if game quit operation is ordered. (Only for Pygame) """
        if self.is_pyodide or not self.visualize:
            return False

        _get_event = pygame.event.get

        for event in _get_event():
            if event.type == pygame.QUIT:
                return True

        return False




    async def set_round_mode(self, round_num: int, unit_table: dict, target_list: dict):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates
        """
        self.logger("round", f"Round Mode is now updated to {round_num}")

        if self.is_pyodide:
            pass
            # TODO: call js method

        elif self.visualize:
            self._set_round_caption(round_num)  # update window name

            # arrange aircrafts
            #TODO: write code for this

            # show selected targets and fires
            #TODO: write code for this

            #self._display_update()
            pass

    async def show_score_panel(self, round_num: int, is_win: bool, score: int):
        """ Show Score Panel when a round is finished """
        self.logger("score", f"[{'WIN' if is_win else 'LOSE'}] Round {round_num} finished. Score is {score}.")

        if self.is_pyodide:
            pass
            # TODO: call js method

        elif self.visualize:
            #TODO

            #self._display_update()
            pass

    async def _update_fire_state(self, target_list):
        """ Fire Status Update """
        #TODO
        pass

    async def _move_object_to(self, obj_name, new_latitude, new_longitude):
        """ Move object to the given coordinates with asynchronized update operation """
        #TODO
        #self._display_update()
        pass

    async def _update_unit_status(self, unit_table, positions):
        """ Update Game Play Screen """
        # TODO
        pass

    async def _update_play_time(self, current_time: str):
        """ Update Game Play Time on the Screen """
        # TODO
        pass
