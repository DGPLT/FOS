# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : app.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from functools import wraps

from display.components import GameVisualizer
from round.scenario import GameScenarios
from api.api_resolver import ApiResolver


def run_simulator(host="", port=0, visualize=True, logging=True):
    if not host:
        host = input("Please specify a host to connect to: ")

    if not port:
        port = int(input("Please set a port of the server to connect to: "))

    # Initialize
    visualizer = GameVisualizer(visualize=visualize, logging=logging)
    scenario = GameScenarios()
    api = ApiResolver()
    api.set_host_addr(host, port)

    def decorator(main):
        @wraps(main)
        async def wrapper(*args, **kwargs):
            # Connect to the server
            await api.connect()
            while True:
                # Run the game
                if not await scenario.run_game(api, visualizer):
                    break
                visualizer.clock.tick(60)  # Set FPS 60
                main(visualizer=visualizer, *args, **kwargs)
            # Disconnect from the server
            await api.disconnect()
        return wrapper
    return decorator
