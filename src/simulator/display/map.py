# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game MAP Design
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PIXEL_EXPANSION = 2.3
MAX_CORDINATION = 300
SCREEN_WIDTH = int(MAX_CORDINATION * PIXEL_EXPANSION)
SCREEN_HEIGHT = int(MAX_CORDINATION * PIXEL_EXPANSION)

""" will make this a class attribute in visualize
# list of dynamic objects
fire = []  # [fire1, fire2, fire3, ...]
aircraft = {}  # {"D1-A": _, ...}
"""

# Cordinates
# from config.coordinates import coordinates

""" map loading inside components
def load_map(pygame):
     "Load map objects from resource files (Initialize)"
    load = pygame.image.load

    # static objects
    background = load("res/FOS_BACKGROUND.png")
    #.......
    #TODO: Load more and fix coordinates

    # dynamic objects
    fire.extend([load("res/fire.png") for _ in range(9)])
    aircraft.update({})
    #TODO: Load more
    
"""

class Aircraft(): # class for managing base aircraft

    def __init__(self):
        self.rotation = 0
        self.latitude = 0
        self.longitude = 0
        self.image = None
