import asyncio

# Try explicitly to declare all your globals at once to facilitate compilation later.
#some globals
COUNT_DOWN = 3

# Do init here and load any assets right now to avoid lag at runtime or network errors.
#some initialization

async def main():
    global COUNT_DOWN

    COUNT_DOWN = 3

    while True:

        # Do your rendering here, note that it's NOT an infinite loop,
        # and it is fired only when VSYNC occurs
        # Usually 1/60 or more times per seconds on desktop, maybe less on some mobile devices

        print(f"Hello[{COUNT_DOWN}] from Python")

        await asyncio.sleep(0)  # Very important, and keep it 0

# This is the program entry point:
asyncio.run(main())

# Do not add anything from here
# asyncio.run is non-blocking on pygame-wasm
