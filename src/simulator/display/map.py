# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game MAP Design
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json

PIXEL_EXPANSION = 2.3
MAX_CORDINATION = 300
SCREEN_WIDTH = MAX_CORDINATION * PIXEL_EXPANSION
SCREEN_HEIGHT = MAX_CORDINATION * PIXEL_EXPANSION


# list of static objects (not moving)
background = None
lake = None
base_a = None
base_b = None
base_c = None
#TODO: Add 

# list of dynamic objects
fire = []  # [fire1, fire2, fire3, ...]
aircraft = {}  # {"D1-A": _, ...}

# Cordinates
cordinates = json.loads("config/coordinates.json")


def load_map(pygame):
    """ Load map objects from resource files (Initialize) """
    load = pygame.image.load

    # static objects
    global background, lake, base_a, base_b, base_c
    background = load("res/background.png")
    #.......
    #TODO: Load more and fix coordinates

    # dynamic objects
    fire.extend([load("res/fire.png") for _ in range(9)])
    aircraft.update({})
    #TODO: Load more

