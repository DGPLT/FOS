# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : con_connector.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : AI/ML Controller Connector
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import asyncio


class ConnectionBuilder(object):
    """ Open client connection to remote controller server asynchronously """
    SIZE = 1024
    ENCODING = 'utf8'

    def __init__(self, host: str = "", port: int = 0):
        if not host:
            self._server_ip: str = "127.0.0.1"
        
        if not port:
            self._server_port: int = 8080
        
        self._reader: asyncio.StreamReader
        self._writer = asyncio.StreamWriter

    @property
    def server_addr(self):
        return (self._server_ip, self._server_port)

    def set_server_ip(self, server_ip):
        self._server_ip: str = server_ip

    def set_server_port(self, server_port):
        self._server_port: int = server_port

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(*self.server_addr)

    async def send(self, msg):
        self._writer.write(msg.encode(self.ENCODING))
        await self._writer.drain()
    
    async def recv(self) -> str:
        data = await self._reader.read(self.SIZE)
        
        if not data:
            raise Exception("Socket connection closed unexpectedly.")
        
        return data.decode(self.ENCODING)


if __name__ == "__main__":
    controller = ConnectionBuilder()

    async def run_client():
        await controller.connect()

        await controller.send("Hello, world!")
        data = await controller.recv()
        print("Recdived:", data)

        await controller.send("quit")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_client())
