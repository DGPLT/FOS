# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Game CLI Log Console Interface & GUI Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import json
from datetime import datetime


class GameVisualizer(object):
    """ Game Visualizer Interface """
    _PIXEL_EXPANSION = 2.3
    _MAX_CORDINATION = 300
    _SCREEN_WIDTH = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_HEIGHT = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_SIZE = (_SCREEN_WIDTH, _SCREEN_HEIGHT)

    is_pyodide: bool = sys.platform == "emscripten" or "pyodide" in sys.modules
    visualize = False

    def __init__(self, logging: bool = True):
        self.logging: bool = logging
        self._log_file = None

        if logging:
            self._log_file = open("play_log.json", "w+")
            self._log_file.write(f"['{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}, Python {sys.version}']")

    def __del__(self):
        if self.logging:
            self._log_file.close()

    def logger(self, title, msg):
        print(title.upper()+": "+msg, flush=True)

        if self.logging:
            if title == "round":
                self._log_file.seek(1)
                self._log_file.write("{'round': '"+msg+"'}, ")
            elif msg[0] in ("{", "[") and msg[-1] in ("}", "]"):
                self._log_file.seek(2)
                self._log_file.write(f", '{title}': {msg}")
            else:
                self._log_file.seek(2)
                self._log_file.write(f", '{title}': '{msg}'")

    async def set_round_mode(self, round_num: int, unit_table: dict, target_list: dict):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates
        """
        self.logger("round", f"Round Mode is now updated to {round_num}")

    async def show_score_panel(self, round_num: int, is_win: bool, score: int):
        """ Show Score Panel when a round is finished """
        self.logger("score", f"[{'WIN' if is_win else 'LOSE'}] Round {round_num} finished. Score is {score}.")

    async def _update_fire_state(self, target_list):
        """ Fire Status Update """
        pass

    async def _move_object_to(self, obj_name, new_latitude, new_longitude):
        """ Move object to the given coordinates with asynchronized update operation """
        pass

    async def _update_unit_status(self, unit_table, positions):
        """ Update Game Play Screen """
        pass

    async def _update_play_time(self, current_time: str):
        """ Update Game Play Time on the Screen """
        pass

    async def apply_dataset(self, target_list, unit_table, positions):
        """ Apply datas to Visualizer
        * Internally, call _update_unit_status and _update_fire_state
        * Add Point-in-time data to the logger
        """
        dataset = {'targets': target_list.to_json(), 'unit_table': json.dumps(unit_table)}
        self.logger(unit_table.current_time, json.dumps(dataset))

        await self._update_play_time(unit_table.current_time)

    async def add_order_log(self, order_xml: str, current_time: str):
        """ Update Order Status Log Sheet """
        self.logger("order_"+current_time, order_xml)
