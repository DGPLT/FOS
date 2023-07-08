# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : run.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : Python Runner for Desktop Application
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import asyncio

from src.simulator.app import run_simulator, GameVisualizer


def get_args() -> dict[str: str, str: int, str: bool, str: bool]:
    result = {"host": "", "port": 0, "visualize": True, "logging": True}

    argv = sys.argv[1:]
    for index, arg in enumerate(argv):
        if arg == "help" or arg == "-help" or arg == "-h" or arg == "--help":
            print("""Usage:
            --help : to list all available
            --host [IP Address, Str] : host to connect to
            --port [Port, Int] : port to connect to
            --visualize [0/1] : visualize or not
            --logging [0/1] : enable log printing using stdout or not
            """)
            sys.exit(0)

        match (arg.startswith("--"), arg):
            case True, "--host":
                result["host"] = argv[index + 1]
            case True, "--port":
                result["port"] = int(argv[index + 1])
            case True, "--visualize":
                result["visualize"] = bool(int(argv[index + 1]))
            case True, "--logging":
                result["logging"] = bool(int(argv[index + 1]))

    return result


@run_simulator(**get_args())
async def main(visualizer: GameVisualizer):
    if visualizer.visualize:
        visualizer.clock.tick(60)  # Set FPS 60

        if visualizer.is_quit_pressed:
            print("Game Exit pressed...")
            sys.exit(0)

    await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
