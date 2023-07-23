# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : entities.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Waters, Nathaniel
Description : Game Entities
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import pygame


class Aircraft:
    """ class for managing base aircraft """
    def __init__(self):
        self.rotation = 0
        self.latitude = 0
        self.longitude = 0
        self.image = None


class Fire(pygame.sprite.Sprite):
    def __init__(self, width, height):
        """ Constructor. Pass in its x and y position """

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
