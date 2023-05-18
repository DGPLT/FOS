# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game CLI Log Console Interface & GUI Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import map as maps


class GameVisualizer(object):
    """ Game Visualizer Interface with PyGame Library """
    fire = [False, False, False, False, False, False, False, False, False] # fire is loaded based on bool position
    Targets = [
            [280, 20],
            [280, 60],
            [280, 100],
            [240, 20],
            [240, 60],
            [240, 100],
            [200, 20],
            [200, 60],
            [200, 100]
        ] # position index for fire
    T1, T2, T3, T4, T5, T6, T7, T8, T9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    fire_sheet = [T1, T2, T3, T4, T5, T6, T7, T8, T9] # pre pygame bucket for fire sprites

    air_sheet = []
    count = 0
    for i in range(3):
        count += 1
        for i in range(10):
            if count == 1:
                air_sheet.append("D" + str(i + 1))
            elif count == 2:
                air_sheet.append("H" + str(i + 1))
            else:
                air_sheet.append("A" + str(i + 1))

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

            self.fire_group = pygame.sprite.Group()

            class Fire(pygame.sprite.Sprite):

                # Constructor. Pass in its x and y position
                def __init__(self, width, height):
                    # Call the parent class (Sprite) constructor
                    pygame.sprite.Sprite.__init__(self)
                    super().__init__()

                    # Create an image of the fire
                    # This could also be an image loaded from the disk.
                    self.image = pygame.image.load("res/Fire1.png")

                    # Fetch the rectangle object that has the dimensions of the image
                    # Update the position of this object by setting the values of rect.x and rect.y
                    self.rect = self.image.get_rect()
                    self.rect.x = width
                    self.rect.y = height


            temp = []
            for i in self.fire_sheet:
                i = Fire(self.Targets[self.fire_sheet.index(i)][0], self.Targets[self.fire_sheet.index(i)][1])
                temp.append(i)
            self.fire_sheet = temp

            self._pygame = pygame
            self._get_event = pygame.event.get
            self._display_update = pygame.display.update
            self._pygame_QUIT = pygame.QUIT
            self.clock = pygame.time.Clock()

            pygame.init()
            self._set_round_caption(0)
            self._screen = pygame.display.set_mode((maps.SCREEN_WIDTH, maps.SCREEN_HEIGHT))
            
            # load map and other images
            self.background_i = pygame.image.load("res/FOS_BACKGROUND.png")
            self.background_i = pygame.transform.scale(self.background_i, (maps.SCREEN_WIDTH, maps.SCREEN_HEIGHT))
            self.drone_i = pygame.image.load("res/drone1.png")
            self.heli_i = pygame.image.load("res/heli1.png")
            self.plane_i = pygame.image.load("res/plane1.png")
            self.fire_i = pygame.image.load("res/Fire1.png")

            self.assign_aircraft(self.air_sheet) # assign class to each aircraft
            #open the window
            self.is_quit_pressed()


    def is_quit_pressed(self) -> bool: # request to rename to window_start
        """ Check if game quit operation is ordered. """
        while self.visualize:
            self._screen.blit(self.background_i, (0, 0))
            for event in self._get_event():
                if event.type == self._pygame_QUIT:
                    self.visualize = False
                    return True
            self._display_update()
        self._pygame.quit()


    def _set_round_caption(self, round: int):
        self._pygame.display.set_caption("Fire Operation Simulator - Round " + str(round))

    def set_round_mode(self, round: int, unit_table: dict, target_list: dict):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates # what does this mean? and unit tabe import?
        """
        if self.logging:
            print(f"Round Mode is now updated to {round}")
        
        if self.visualize: # i don't know why this would be done here
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

        if self.visualize: # i would need to make more images for this and caption text
            #TODO

            self._display_update()

    def assign_aircraft(self, air_sheet):
        temp = []
        for i in air_sheet:
            if "D" in i:
                i = maps.Aircraft()
                i.image = self.drone_i
                temp.append(i)
            elif "H" in i:
                i = maps.Aircraft()
                i.image = self.heli_i
                temp.append(i)
            elif "A" in i:
                i = maps.Aircraft()
                i.image = self.plane_i
                temp.append(i)
            else:
                print("error in parsing air sheet")
            self.air_sheet = temp

    async def update_fire_state(self, fire):
        """ Fire Status Update """
        count = 0
        for i in fire:
            if i:
                print("im in here"+str(count))
                self.fire[i] = i
                self.fire_group.add(self.fire_sheet[count])
            count += 1
        self.fire_group.draw(self._screen)

    async def move_object_to(self, obj_name, new_latitude, new_longitude):
        """ Move object to the given coordinates with asynchronized update operation """
        #TODO
        self._display_update()


game = GameVisualizer()
