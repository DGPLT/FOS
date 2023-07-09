# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : con_connector.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by MUN, CHAEUN
Description : AI/ML Controller Connector
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import asyncio
import json
from typing import Callable
import xml.etree.ElementTree as elemTree

from .con_connector import ConnectionBuilder


class ApiResolver:
    """ Asynchronous API resolver """

    def __init__(self):
        self._controller = ConnectionBuilder()
        self._connected = False

    @property
    def is_connected(self):
        return self._connected
    
    def set_host_addr(self, host, port):
        self._controller.set_server_ip(host)
        self._controller.set_server_port(port)

    async def connect(self) -> bool:
        """ Connect to the server """
        while True:
            try:
                await self._controller.connect()
                self._connected = True
                await self._controller.send("!CONNECTED!")
                print(f"Server connection has been done successfully.")
                return True
            except ConnectionRefusedError as e:
                print(e)
                print("Server seems to be down or yet opened. Try reconnecting...")
                await asyncio.sleep(0)
            except KeyboardInterrupt as e:
                print("Server connection was interrupted.")
                return False

    async def disconnect(self):
        await self._controller.send("/disconnect")
        raise Exception("Server Connection is lost. Terminating...")

    async def resolve(self) -> tuple[str, str, Callable]:
        """ API resolve function
        /start
        /data/aircraft_specsheet
        /data/target_list
        /data/unit_table
        /order/<XML>  => after validating the XML send order status like 200 or 403
        /result
        /disconnect

        :return: (request, option, function)
        """
        if not self.is_connected:
            raise Exception("Connection is not yet established.")
        
        request = await self._controller.recv()
        if not request:
            del self._controller
            self._controller = ConnectionBuilder()
            self._connected = False

        if request.startswith("/order/"):
            xml = request[len("/order/"):]
            # validate xml
            try:
                elemTree.fromstring(xml)
            except Exception as e:  # format error
                await self._controller.send(json.dumps({"code": 400, "message": str(e)}))
            return "/order", request[len("/order/"):], self._send_operation_result
        
        match request:
            case "/start":
                return request, "", self._send_game_start_signal
            case "/data/aircraft_specsheet":
                return "/data", "aircraft_specsheet", self._send_aircraft_specsheet
            case "/data/target_list":
                return "/data", "target_list", self._send_target_list
            case "/data/unit_table":
                return "/data", "unit_table", self._send_unit_table
            case "/result":
                return request, "", self._send_game_result_by_round
            case "/disconnect":
                await self.disconnect()
            case _:
                await self._controller.send(json.dumps({"code": 404, "message": "Not Found"}))
                return request, "", lambda **kwargs: None

    async def _send_game_start_signal(self, **kwargs):
        """ Send a game start signal
        data = { "round": int }
        """
        if "code" in kwargs and kwargs["code"] == 403:
            await self._controller.send(json.dumps({"code": 403, "message": "Forbidden"}))
        elif "code" in kwargs and kwargs["code"] == 302:
            await self._controller.send(json.dumps({"code": 302, "message": kwargs.get("redi_url", "Redirect")}))
        else:
            await self._controller.send(json.dumps(
                {"code": 200, "message": f"Round {kwargs['round']} is ready.", "data": kwargs}))

    async def _send_aircraft_specsheet(self, **kwargs):
        """ Send the spec sheet of aircraft
        data = {} --- aircraft_spec_sheet.py
        """
        if "code" in kwargs and kwargs["code"] == 302:
            await self._controller.send(json.dumps({"code": 302, "message": kwargs.get("redi_url", "Redirect")}))
        elif "code" in kwargs and kwargs["code"] == 401:
            await self._controller.send(json.dumps({"code": 401, "message": "Unauthorized"}))
        else:
            await self._controller.send(json.dumps(
                {"code": 200, "message": "Success", "data": kwargs["spec_sheet"]}))

    async def _send_target_list(self, **kwargs):
        """ Send the current target status
        data = {} --- locations.py
        """
        if "code" in kwargs and kwargs["code"] == 302:
            await self._controller.send(json.dumps({"code": 302, "message": kwargs.get("redi_url", "Redirect")}))
        elif "code" in kwargs and kwargs["code"] == 401:
            await self._controller.send(json.dumps({"code": 401, "message": "Unauthorized"}))
        else:
            await self._controller.send(json.dumps(
                {"code": 200, "message": "Success", "data": kwargs["target_list"]}))

    async def _send_unit_table(self, **kwargs):
        """ Send the current unit table status
        data = {} --- unit_table.py
        """
        if "code" in kwargs and kwargs["code"] == 302:
            await self._controller.send(json.dumps({"code": 302, "message": kwargs.get("redi_url", "Redirect")}))
        elif "code" in kwargs and kwargs["code"] == 401:
            await self._controller.send(json.dumps({"code": 401, "message": "Unauthorized"}))
        else:
            await self._controller.send(json.dumps(
                {"code": 200, "message": "Success", "data": kwargs["unit_table"]}))

    async def _send_operation_result(self, **kwargs):
        """ Send operation apply trial result of an order
        data = { "code": 200, "message": "Success" } or { "code": 500, "message": "?????" }
        """
        await self._controller.send(json.dumps(kwargs))

    async def _send_game_result_by_round(self, **kwargs):
        """ Send game result by round
        data = {
            "round": int, "is_win": bool, "score": int
        }
        """
        if "code" in kwargs and kwargs["code"] == 403:
            await self._controller.send(json.dumps({"code": 403, "message": "Forbidden"}))
        elif "code" in kwargs and kwargs["code"] == 401:
            await self._controller.send(json.dumps({"code": 401, "message": "Unauthorized"}))
        else:
            await self._controller.send(json.dumps(
                {"code": 200, "message": f"Round {kwargs['round']} is finished.", "data": kwargs}))
