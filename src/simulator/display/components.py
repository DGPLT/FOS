# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game CLI Log Console Interface & GUI Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import src.simulator.display.map as maps


class GameVisualizer(object):
    """ Game Visualizer Interface with PyGame Library """

    def __init__(self, logging: bool = True, visualize: bool = True):
        """
        :param logging: bool, if True then logging to stdout won't be operated.
        """
        self.logging: bool = logging
        self.visualize: bool = visualize
        self._display_update = lambda: None

        if visualize:
            # import pygame library only when visualizer is enabled
            import pygame
            self._pygame = pygame
            self._get_event = pygame.event.get
            self._display_update = pygame.display.update
            self._pygame_QUIT = pygame.QUIT
            self.clock = pygame.time.Clock()

            pygame.init()
            self._set_round_caption(0)
            self._screen = pygame.display.set_mode((maps.SCREEN_WIDTH, maps.SCREEN_HEIGHT))
            
            # load map
            maps.load_map(self._pygame)

    def is_quit_pressed(self) -> bool:
        """ Check if game quit operation is ordered. """
        if not self.visualize:
            return False

        for event in self._get_event():
            if event.type == self._pygame_QUIT:
                return True
        
        return False

    def _set_round_caption(self, round: int):
        self._pygame.display.set_caption("Fire Operation Simulator - Round " + round)

    def set_round_mode(self, round: int, unit_table: dict, target_list: dict):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates
        """
        if self.logging:
            print("Round Mode is now updated to " + round)
        
        if self.visualize:
            self._set_round_caption(round)  # update window name

            # arrange aircrafts
            #TODO: write code for this 

            # show selected targets and fires
            #TODO: write code for this

            self._display_update()
    
    def show_score_panel(self, round: int, score: int):
        """ Show Score Panel when a round is finished """
        if self.logging:
            print(f"Round {round} finished. Score is {score}.")

        if self.visualize:
            

            self._display_update()

    def update_fire_state(self):


    
    def move_object_to(self, obj_name, new_location):

        self._display_update()