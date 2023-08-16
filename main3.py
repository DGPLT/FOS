# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : run.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Python Runner for Web Application
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import asyncio
from enum import Enum


# Try explicitly to declare all your globals at once to facilitate compilation later.
looper = []  # message queue for ui loop


class Handle(Enum):
    PAUSE = 0
    START = 1


def pause(): looper.append(Handle.PAUSE)


def start(): looper.append(Handle.START)


# Do init here and load any assets right now to avoid lag at runtime or network errors.
import src.simulator.app3 as app


async def init():
    await app.GameVisualizer.initializer()


@app.run_simulator(host="", port=0, visualize=True, logging=True, use_websocket=True)
async def main(visualizer: app.GameVisualizer):
    """ If this app runs on Pyodide, NO-GUI Option will be ignored. """

    # Do your rendering here, note that it's NOT an infinite loop,
    # and it is fired only when VSYNC occurs
    # Usually 1/60 or more times per seconds on desktop, maybe less on some mobile devices

    while True:
        await asyncio.sleep(0)  # Very important, and keep it 0

        state = visualizer.get_game_state()
        if looper:
            msg = looper.pop()
            if msg == Handle.PAUSE and state != state.PAUSE:
                await visualizer.set_game_state(state.PAUSE)
                print("Game Paused...")
                continue
            elif msg == Handle.START and state == state.PAUSE:
                await visualizer.set_game_state(state.RUNNING)
                print("Resume Game!")
                break
        else:
            if state != state.PAUSE:
                break
