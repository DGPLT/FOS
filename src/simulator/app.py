# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : app.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Simulator Main
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from functools import wraps

from src.simulator.display.components import GameVisualizer
from src.simulator.round.scenario import GameScenarios
from src.simulator.api.api_resolver import ApiResolver


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
            # Start new round
            await scenario.start_new_round(api, visualizer)
            while True:
                # Run the game
                if not await scenario.run_game(api, visualizer):
                    # Show Result Panel
                    if await scenario.end_this_round(api, visualizer):  # Win
                        # Go next round
                        await scenario.start_new_round(api, visualizer)
                    else:  # Lose or Game Finished
                        break
                main(visualizer=visualizer, *args, **kwargs)
            # Disconnect from the server
            try:
                await api.disconnect()
            except Exception:
                print("Server connection is closed properly.")
        return wrapper
    return decorator
