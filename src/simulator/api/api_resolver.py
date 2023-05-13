# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : con_connector.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : AI/ML Controller Connector
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import asyncio

from .con_connector import ConnectionBuilder

class ApiResolver():
    """ Asynchronous API resolver """

    def __init__(self):
        self._controller = ConnectionBuilder()
        self._connected = False
    
    @property
    def is_connected(self):
        return self._connected
    
    def set_host_addr(self, host, port):
        self._controller.set_host_ip(host)
        self._controller.set_host_port(port)
    
    async def connect(self) -> bool:
        """ Connect to the server """
        while True:
            try:
                self._controller.connect()
                self._connected = True
                self.send("!CONNECTED!")
                print(f"Server connection has been done successfully.")
                return True
            except ConnectionRefusedError as e:
                print(e)
                print("Server seems to be down or yet opened. Try reconnecting...")
                asyncio.sleep(0)
            except KeyboardInterrupt as e:
                print("Server connection was interrupted.")
                return False

    async def disconnect(self):
        #TODO
        pass

    async def resolve(self) -> tuple(str, function):
        """ API resolve function
        /start
        /data/aircraft_specsheet
        /data/target_list
        /data/unit_table
        /order/<XML>  => after validating the XML send order status like 200 or 403
        /result
        /disconnect
        """
        if not self.is_connected():
            raise Exception("Connection is not yet established.")
        
        request = self._controller.recv()
        if not request:
            del self._controller
            self._controller = ConnectionBuilder()
            self._connected = False

        if request.startwith("/order/"):
            return "/order", self._recv_operation_order
        
        match (request):
            case "/start":
                return request, self._send_game_start_signal
            case "/data/aircraft_specsheet":
                return request, self._send_aircraft_specsheet
            case "/data/target_list":
                return request, self._send_target_list
            case "/data/unit_table":
                return request, self._send_unit_table
            case "/result":
                return request, self._send_operation_result
            case "/disconnect":
                await self._disconnect()
                return request, lambda: None

    
    async def _send_game_start_signal(self, data):
        """ Send a game start signal
        data = { round: 1 }
        """
        #TODO
        pass

    async def _send_aircraft_specsheet(self, data):
        """ Send the spec sheet of aircrafts
        data = {} --- aircraft_spec_sheet.json
        """
        #TODO
        pass

    async def _send_target_list(self, data):
        """ Send the current target status
        data = {

        }
        """
        #TODO
        pass

    async def _send_unit_table(self, data):
        """ Send the current unit table status
        data = {

        }
        """
        #TODO
        pass

    async def _recv_operation_order(self, result):
        """ Recv operation tasking order sheet
        result = {

        }
        """
        #TODO
        pass

    async def _send_operation_result(self, data):
        """ Send operation result of an order
        data = {

        }
        """
        #TODO
        pass
