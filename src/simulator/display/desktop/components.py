# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Game CLI Log Console Interface & GUI Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from src.simulator.display.components import GameVisualizer


class PyArcadeVisualizer(GameVisualizer):
    _PIXEL_EXPANSION = 2.3
    _MAX_CORDINATION = 300
    _SCREEN_WIDTH = round(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_HEIGHT = round(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_SIZE = (_SCREEN_WIDTH, _SCREEN_HEIGHT)

    visualize = True

    def __init__(self, logging: bool = True):
        super().__init__(logging)

        self._display_update = lambda: None
        self._display_update = pygame.display.update
        self.clock = pygame.time.Clock()

        pygame.init()
        self._set_round_caption(0)
        self._screen = pygame.display.set_mode(_SCREEN_SIZE)

    def is_quit_pressed(self) -> bool:
        """ Check if game quit operation is ordered. (Only for Pygame) """

        _get_event = pygame.event.get

        for event in _get_event():
            if event.type == pygame.QUIT:
                return True

        return False

    def _set_round_caption(self, round_num: int):
        if self.visualize and not self.is_pyodide:
            pygame.display.set_caption(f"Fire Operation Simulator - Round {round_num}")




    async def set_round_mode(self, round_num: int, unit_table, target_list):
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

    async def _update_unit_status(self, unit_table, positions: dict[str, tuple[int, int]]):
        """ Update Game Play Screen """
        # TODO
        pass

    async def _update_play_time(self, current_time: str):
        """ Update Game Play Time on the Screen """
        # TODO
        pass

    async def _display_update(self):
        """ Refresh/Update Screen """
        pass
