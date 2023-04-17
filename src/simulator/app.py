import os
import sys
import socket
import arcade
from threading import Thread
from multiprocessing import Process

from src.simulator.display.map import Map1
from src.config import connection_config as con_config


def interrupt(on_key_press, on_key_release):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as simulator:
        simulator.bind(con_config.ADDR)
        simulator.listen()
        print("Connecting to Controller...")

        while True:
            controller, controller_addr = simulator.accept()
            msg = controller.recv(con_config.SIZE)
            print(f"Controller({controller_addr}) Connected:", msg.decode())
            controller.send("Welcome to the game!".encode())
            
            while True:
                data = controller.recv(con_config.SIZE)
                if not data: break
                try:
                    pressed, key = map(int, data.decode().split("/"))
                except:
                    continue
                if pressed:
                    on_key_press(key, "")
                else:
                    on_key_release(key, "")


def main():
    screen = Map1()
    screen.setup()

    keyboard_interrupt = Thread(target=interrupt, args=(screen.on_key_press, screen.on_key_release))
    keyboard_interrupt.start()

    arcade.run()


if __name__ == '__main__':
    main()
