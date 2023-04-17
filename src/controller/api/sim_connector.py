"""
Platformer Template
"""
import arcade

# --- Constants
SCREEN_TITLE = "Controller"

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 2000

import socket
from src.config import connection_config as con_config

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller.connect(con_config.ADDR)
controller.send("Hello World!".encode())
print("Simulator Connected: " + controller.recv(con_config.SIZE).decode())


class Controller_Window(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W \
        or key == arcade.key.LEFT or key == arcade.key.A \
        or key == arcade.key.RIGHT or key == arcade.key.D:
            controller.send(f"1/{key}".encode())

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W \
        or key == arcade.key.LEFT or key == arcade.key.A \
        or key == arcade.key.RIGHT or key == arcade.key.D:
            controller.send(f"1/{key}".encode())


def main():
    con = Controller_Window()
    arcade.run()


if __name__ == "__main__":
    main()
