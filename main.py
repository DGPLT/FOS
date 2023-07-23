# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : run.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Python Runner for Web Application
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import asyncio

# Try explicitly to declare all your globals at once to facilitate compilation later.
#some globals

# Do init here and load any assets right now to avoid lag at runtime or network errors.
import src.simulator.app as app


@app.run_simulator(host="", port=0, visualize=True, logging=True)
async def main(visualizer: app.GameVisualizer):
    """ If this app runs on Pyodide, NO-GUI Option will be ignored. """

    # Do your rendering here, note that it's NOT an infinite loop,
    # and it is fired only when VSYNC occurs
    # Usually 1/60 or more times per seconds on desktop, maybe less on some mobile devices

    await asyncio.sleep(0)  # Very important, and keep it 0


# This is the program entry point:
asyncio.run(main())

# Do not add anything from here
# asyncio.run is non-blocking on pygame-wasm
