# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : app.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from functools import wraps
import asyncio

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
            await scenario.start_new_round(visualizer)
            while True:
                # Run the game
                if not await scenario.run_game(api, visualizer):
                    cur_round = scenario.current_round
                    # Show Result Panel
                    await visualizer.show_score_panel(cur_round.round_num, cur_round.is_win, cur_round.score)
                    await asyncio.sleep(30)  # wait for 30 sec
                    if cur_round.is_win and cur_round.round_num < 3:  # Win
                        # Go next round
                        await scenario.start_new_round(visualizer)
                    else:  # Lose or Game Finished
                        break
                visualizer.clock.tick(60)  # Set FPS 60
                main(visualizer=visualizer, *args, **kwargs)
            # Disconnect from the server
            await api.disconnect()
        return wrapper
    return decorator
