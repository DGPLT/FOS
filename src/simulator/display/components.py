# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game CLI Log Console Interface & GUI Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys

_PIXEL_EXPANSION = 2.3
_MAX_CORDINATION = 300
_SCREEN_WIDTH = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
_SCREEN_HEIGHT = int(_MAX_CORDINATION * _PIXEL_EXPANSION)
_SCREEN_SIZE = (_SCREEN_WIDTH, _SCREEN_HEIGHT)

js = None

pygame = None
load_image = None
entities = None


def load_js():
    """ JS Object Loader """
    global js
    if js is None:
        import js as js_module
        js = js_module


def load_pygame():
    """ PyGame Loader """
    global pygame, load_image, entities
    if pygame is None:
        import pygame as pygame_module
        pygame = pygame_module
        load_image = pygame.image.load
        from . import entities as ent
        entities = ent


class GameVisualizer(object):
    """ Game Visualizer Interface with PyGame Library """

    def __init__(self, logging: bool = True, visualize: bool = True):
        """
        :param logging: bool, if True then logging to stdout won't be operated.
        """
        self.logging: bool = logging
        self.visualize: bool = visualize
        self.is_pyodide: bool = sys.platform == "emscripten" or "pyodide" in sys.modules
        self._display_update = lambda: None

        if self.is_pyodide:
            load_js()

        if visualize and not self.is_pyodide:
            # import pygame library only when visualizer is enabled
            load_pygame()

            self._display_update = pygame.display.update
            self.clock = pygame.time.Clock()

            pygame.init()
            self._set_round_caption(0)
            self._screen = pygame.display.set_mode(_SCREEN_SIZE)

    def is_quit_pressed(self) -> bool:
        """ Check if game quit operation is ordered. (Only for Pygame) """
        if self.is_pyodide or not self.visualize:
            return False

        _get_event = pygame.event.get

        for event in _get_event():
            if event.type == pygame.QUIT:
                return True

        return False

    def _set_round_caption(self, round_num: int):
        if self.visualize and not self.is_pyodide:
            pygame.display.set_caption(f"Fire Operation Simulator - Round {round_num}")

    async def set_round_mode(self, round_num: int, unit_table: dict, target_list: dict):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates
        """
        if self.logging:
            print(f"Round Mode is now updated to {round_num}")

        if self.is_pyodide:
            pass
            # TODO: call js method

        elif self.visualize:
            self._set_round_caption(round_num)  # update window name

            # arrange aircrafts
            #TODO: write code for this 

            # show selected targets and fires
            #TODO: write code for this

            self._display_update()

    async def show_score_panel(self, round_num: int, is_win: bool, score: int):
        """ Show Score Panel when a round is finished """
        if self.logging:
            print(f"[{'WIN' if is_win else 'LOSE'}] Round {round_num} finished. Score is {score}.")

        if self.is_pyodide:
            pass
            # TODO: call js method

        elif self.visualize:
            #TODO

            self._display_update()

    async def update_fire_state(self, fire):
        """ Fire Status Update """
        #TODO

    async def move_object_to(self, obj_name, new_latitude, new_longitude):
        """ Move object to the given coordinates with asynchronized update operation """
        #TODO
        self._display_update()
