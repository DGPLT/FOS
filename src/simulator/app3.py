# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : app.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Simulator Main
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from functools import wraps

from src.simulator.display import get_impl
from src.simulator.round.scenario import GameScenarios
from src.simulator.api.api_resolver import ApiResolver


def run_simulator(host="", port=0, visualize=True, logging=True, use_websocket=False):
    if not host:
        host = input("Please specify a host to connect to: ")
        if host == "rtc":
            port = host

    if not port:
        port = int(input("Please set a port of the server to connect to: "))

    # Initialize
    global GameVisualizer
    GameVisualizer = get_impl(visualize=visualize)
    visualizer1 = GameVisualizer(logging=logging, canvas_id="gameview1", unit_table_id="unit1", target_table_id="target1",
                                 spec_sheet_id="specsheet", game_state_id="gamestate", game_time_id="gametime1",
                                 score_modal_id="scorePanelModal", score_panel_id="score-panel-text1",
                                 api_log_id="output", fos_version_info="fos_version_info")
    visualizer2 = GameVisualizer(logging=logging, canvas_id="gameview2", unit_table_id="unit2", target_table_id="target2",
                                 spec_sheet_id="specsheet", game_state_id="gamestate", game_time_id="gametime2",
                                 score_modal_id="scorePanelModal", score_panel_id="score-panel-text2",
                                 api_log_id="output", fos_version_info="fos_version_info")
    visualizer3 = GameVisualizer(logging=logging, canvas_id="gameview3", unit_table_id="unit3", target_table_id="target3",
                                 spec_sheet_id="specsheet", game_state_id="gamestate", game_time_id="gametime3",
                                 score_modal_id="scorePanelModal", score_panel_id="score-panel-text3",
                                 api_log_id="output", fos_version_info="fos_version_info")
    scenario = GameScenarios()
    api1 = ApiResolver(use_websocket)
    api1.set_host_addr(host, port)
    api2 = ApiResolver(use_websocket)
    api2.set_host_addr(host, port+1)
    api3 = ApiResolver(use_websocket)
    api3.set_host_addr(host, port+2)

    def decorator(main):
        @wraps(main)
        async def wrapper(*args, **kwargs):
            # Connect to the server
            await api1.connect()
            await api2.connect()
            await api3.connect()
            # Start new round
            await scenario.start_new_round(api1, visualizer1)
            await scenario.start_new_round(api2, visualizer2)
            await scenario.start_new_round(api3, visualizer3)
            while True:
                # Run the game
                if not await scenario.run_game(api1, visualizer1) or not await scenario.run_game(api2, visualizer2) \
                        or not await scenario.run_game(api3, visualizer3):
                    # Show Result Panel
                    if await scenario.end_this_round(api1, visualizer1) or await scenario.end_this_round(api2, visualizer2) \
                            or await scenario.end_this_round(api3, visualizer3):  # Win
                        # Go next round
                        await scenario.start_new_round(api1, visualizer1)
                        await scenario.start_new_round(api2, visualizer2)
                        await scenario.start_new_round(api3, visualizer3)
                    else:  # Lose or Game Finished
                        break
                await main(visualizer=visualizer1, *args, **kwargs)
                await main(visualizer=visualizer2, *args, **kwargs)
                await main(visualizer=visualizer3, *args, **kwargs)
            # Disconnect from the server
            try:
                await api1.disconnect()
                await api2.disconnect()
                await api3.disconnect()
            except Exception:
                print("Server connection is closed properly.")
        return wrapper
    return decorator
