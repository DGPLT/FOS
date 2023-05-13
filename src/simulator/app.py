# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : app.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from functools import wraps

from .display.components import GameVisualizer

# Initialization


def run_simulator(host="", port=0, visualize=True, logging=True):
    if not host:
        host = input("Please specify a host to connect to: ")
    
    if not port:
        port = int(input("Please set a port of the server to connect to: "))

    # Initialize
    visualizer = GameVisualizer(visualize=visualize, logging=logging)

    def decorator(main):
        @wraps(main)
        async def wrapper(*args, **kwargs):
            while True:
                visualizer.clock.tick(60)

                main(visualizer=visualizer, *args, **kwargs)
        return wrapper
    return decorator
