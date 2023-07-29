# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : components.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by Myung, Gyung Min
Description : Web Visualization
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from __future__ import annotations

from src.simulator.display.components import GameVisualizer
from src.simulator.unit.aircraft import Aircrafts

import js
import re
import json
import asyncio
import logging
import pkg_resources
from enum import Enum


class JSVisualizer(GameVisualizer):
    _PIXEL_EXPANSION = 0.5
    _MAX_CORDINATION = 1200
    _SCREEN_WIDTH = round(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_HEIGHT = round(_MAX_CORDINATION * _PIXEL_EXPANSION)
    _SCREEN_SIZE = (_SCREEN_WIDTH, _SCREEN_HEIGHT)

    RESOURCE_PATH = "/res/"

    visualize = True

    @classmethod
    async def load_image(cls, route: str):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        img: js.HTMLImageElement = js.Image.new()  # type: ignore

        def on_load(_):
            logging.info(f"filename: {route} loaded")
            if not future.done():
                future.set_result(img)

        def timeout():
            if not future.done():
                logging.error(f"filename: {route} load timeout")
                future.set_result(None)

        img.onload = on_load
        # set timeout of 5 seconds
        loop.call_later(5, timeout)

        img.src = cls.RESOURCE_PATH + route

        return await future

    @classmethod
    @property
    def FIRE_IMG_RES(cls):
        try:
            return cls._FIRE_IMG_RES
        except AttributeError:
            raise AttributeError("The initializer must be executed first.")

    @classmethod
    @property
    def AIRCRAFT_IMG_RES(cls):
        try:
            return cls._AIRCRAFT_IMG_RES
        except AttributeError:
            raise AttributeError("The initializer must be executed first.")

    @classmethod
    async def initializer(cls):
        cls._FIRE_IMG_RES = await cls.load_image(cls.FIRE_IMG_SOURCE)

        get_aircraft_res = lambda _id: _id[0] + "/" + _id[1:] + ".png"
        aircraft_img_poll = {x: cls.load_image(get_aircraft_res(x.split("-")[0])) for x in cls._aircraft_ids}
        cls._AIRCRAFT_IMG_RES = {_id: img for _id, img in zip(aircraft_img_poll.keys(), await asyncio.gather(*aircraft_img_poll.values()))}

    class AircraftModel(Enum):
        # define image size as of when the map size is 300px
        D = (round(16*5), 0)  # (pixel_size, _dum_val)
        H = (round(32*5), 0)
        A = (round(32*5), 1)

        @classmethod
        def get_relative_size(cls, _id) -> int:
            _id = re.split(r"[0-9]", _id.split("-")[0])[0]
            for e in cls:
                if e.name == _id:
                    return round(e.value[0] * JSVisualizer.get_pixel_expansion())
            raise ValueError(f"Cannot find a AircraftModel with id={_id}.")

    class GameState(Enum):
        RUNNING = 0
        END = 1
        ERROR = 2
        PAUSE = 3
        UNKNOWN = 4

        def to_str(self, current_round: int) -> str:
            if self == self.RUNNING:
                return f"🟢 Round {current_round} Running"
            elif self == self.END:
                return f"🔴 Round {current_round} End"
            elif self == self.ERROR:
                return f"🟠 Round {current_round} Error"
            elif self == self.PAUSE:
                return f"🟡 Round {current_round} Pause"
            else:
                return f"⚪ Round {current_round} Unknown"

    class JSElements(object):
        class JSTable(object):
            def __init__(self, table: js.HTMLTableElement):
                self.obj: js.HTMLTableElement = table
                self.ids = []

            def _insert_to_row(self, row: js.HTMLTableRowElement, row_data: list | tuple):
                insertCell = row.insertCell
                for data in row_data:
                    insertCell().innerHTML = str(data)

            def _get_row_obj(self, _id: str) -> js.HTMLTableRowElement:
                if _id not in self.ids:
                    raise KeyError(f"Table Row id={_id} is not exists.")
                return js.document.getElementById(_id)

            def append(self, _id: str, row_data: list | tuple):
                row = self.obj.insertRow()
                row.setAttribute("id", _id)  # type: ignore
                self.ids.append(_id)
                self._insert_to_row(row, row_data)

            def remove(self, _id: str):
                self.ids.remove(_id)
                row = self._get_row_obj(_id)
                row.parentElement.removeChild(row)  # type: ignore

            def update(self, _id: str, row_data: list | tuple):
                if _id not in self.ids:
                    return self.append(_id, row_data)
                row = self._get_row_obj(_id)
                for _ in range(len(row_data)):
                    row.deleteCell(0)  # type: ignore
                self._insert_to_row(row, row_data)

        def __init__(self, canvas_id: str = "gameview", unit_table_id: str = "unit", target_table_id: str = "target",
                     spec_sheet_id: str = "specsheet", game_state_id: str = "gamestate", game_time_id: str = "gametime",
                     score_modal_id: str = "scorePanelModal", score_panel_id: str = "score-panel-text",
                     api_log_id: str = "output", fos_version_info: str = "fos_version_info"):
            getElementById = js.document.getElementById

            self._pixel_expansion = JSVisualizer.get_pixel_expansion()
            self.screen_size = JSVisualizer.get_screen_size()
            self.fire_border_size = round(40 * 4 * self._pixel_expansion)
            self.fire_size = round(74 * 4 * self._pixel_expansion)
            self.get_relative_airc_size = JSVisualizer.AircraftModel.get_relative_size

            self.api_log = js.HTMLElement = getElementById(api_log_id)
            self.api_log_id = api_log_id
            formatting = "[%(levelname)s] %(message)s"
            logging.basicConfig(handlers=[CustomLogHandler(self.api_log)], level=logging.INFO, format=formatting)

            self.canvas_id = canvas_id
            self.canvas: js.CanvasRenderingContext2D = getElementById(canvas_id).getContext("2d")  # type: ignore
            self.unit_table_id = unit_table_id
            self.unit_table: js.HTMLTableElement = getElementById(unit_table_id)  # type: ignore
            self.unit_table_obj = self.JSTable(self.unit_table)
            self.target_table_id = target_table_id
            self.target_table: js.HTMLTableElement = getElementById(target_table_id)  # type: ignore
            self.target_table_obj = self.JSTable(self.target_table)
            self.spec_sheet_id = spec_sheet_id
            self.spec_sheet: js.HTMLTableElement = getElementById(spec_sheet_id)  # type: ignore
            self.spec_sheet_obj = self.JSTable(self.spec_sheet)

            self.background_src = JSVisualizer.BACKGROUND_IMG_SOURCE
            self.background: js.HTMLImageElement = js.Image.new()  # type: ignore
            self.background.src = JSVisualizer.RESOURCE_PATH + self.background_src
            self.background.onload = lambda _: logging.info(f"filename: {self.background_src} loaded")
            self.draw_background()  # type: ignore

            self.game_state = js.HTMLElement = getElementById(game_state_id)  # type: ignore
            self.game_state_id = game_state_id
            self.set_game_state("Initializing...")

            self.fos_version_inf = js.HTMLElement = getElementById(fos_version_info)  # type: ignore
            self.fos_version_inf_id = fos_version_info
            try:
                fos_ver = pkg_resources.get_distribution("fos_simulator").version
            except pkg_resources.DistributionNotFound:
                with open("./config/info.json") as f_info:
                    info = json.load(f_info)
                    fos_ver = info['version']
            self.fos_version_inf.innerHTML = "v" + fos_ver

            self.game_time = js.HTMLElement = getElementById(game_time_id)
            self.game_time_id = game_time_id

            self.score_panel = js.HTMLElement = getElementById(score_panel_id)
            self.score_panel_id = score_panel_id
            self.score_modal = js.HTMLElement = getElementById(score_modal_id)
            self.score_modal_id = score_modal_id

            self.positions: dict[str, tuple[int, int]] = {}
            self.targets = None

            self.update_spec_table(Aircrafts)

        def set_game_state(self, message: str):
            self.game_state.innerHTML = message

        def set_game_time(self, current_time: str):
            self.game_time.innerHTML = current_time

        def set_target_status(self, target_list):
            self.targets = target_list.targets

        def update_spec_table(self, spec_sheet):
            packager = lambda _id, x: (x.type.name, _id, str(x.velocity), str(x.ETRDY), str(x.cost),
                                       x.cover_area.name, str(x.water_tank), str(x.possibility))
            get = spec_sheet.get
            spec = self.spec_sheet_obj
            [spec.update(_id, packager(_id, get(_id))) for _id in spec_sheet.keys()]

        def update_target_table(self, target_list):
            packager = lambda k, o: (str(o.is_targeted), k, str(o.priority) if o.priority == 0 else "",
                                     str(o.lat), str(o.long), o.type.name, str(o.threat), str(o.probability))
            targets = target_list.targets
            target = self.target_table_obj
            [target.update(key, packager(key, targets[key])) for key in targets.keys()]

        def set_aircraft_positions(self, positions: dict[str, tuple[int, int]]):
            self.positions = positions

        def update_unit_table(self, unit_table):
            packager = lambda k, o: (str(o['Ordered']), str(o['Available']), o['ETR'],
                                     o['ETD'], o['ETA'], o['Base'], k, str(round(o['Current Water'], 3)))
            unit = self.unit_table_obj
            [unit.update(key, packager(key, val)) for key, val in unit_table.items()]

        def launch_score_panel(self):
            js.bootstrap.Modal.getOrCreateInstance(self.score_modal).show()

        def append_current_round_score(self, round_num: int, is_win: bool, score: int):
            self.score_panel.innerHTML \
                += f"[{'WIN' if is_win else 'LOSE'}] Round {round_num} Score: {score if is_win else 'None'}<br><br>"

        def append_order_log(self, order_xml: str, current_time: str):  # Cannot be Static
            if order_xml.replace("\n", "").replace(" ", "") != "<operations></operations>":
                logging.info("order_" + current_time + " <XMP>" + order_xml + "</XMP>")

        def draw_background(self):
            self.canvas.drawImage(self.background, 0, 0, *self.screen_size)  # type: ignore

        def draw_aircrafts(self):
            get_relative_size = self.get_relative_airc_size
            AIRCRAFT_IMG_RES = JSVisualizer.AIRCRAFT_IMG_RES
            _PIXEL_EXPANSION = JSVisualizer._PIXEL_EXPANSION
            expansion = self._pixel_expansion
            drawImage = self.canvas.drawImage
            for aid, pos in self.positions.items():
                size = get_relative_size(aid)
                shift = round(size / 2)
                drawImage(AIRCRAFT_IMG_RES[aid], pos[0]*expansion-shift, self.screen_size[1]-pos[1]*expansion-shift, size, size)

        def draw_fires(self):
            if self.targets is None:
                return

            FIRE_IMG_RES = JSVisualizer.FIRE_IMG_RES
            drawImage = self.canvas.drawImage
            self.canvas.strokeStyle = "rgb(230, 87, 81)"  # Cherry Red
            strokeRect = self.canvas.strokeRect
            expansion = self._pixel_expansion
            shift = round(self.fire_size / 2)
            border_shift = round(self.fire_border_size / 2)
            for t in self.targets.keys():
                target = self.targets[t]
                t_type = target.type
                long = round(target.long*expansion)
                lat = self.screen_size[1] - round(target.lat*expansion)
                if t_type != t_type.NONE:
                    # draw red block
                    strokeRect(long-border_shift, lat-border_shift, self.fire_border_size, self.fire_border_size)
                    # show fire
                    if t_type == t_type.FIRE:
                        drawImage(FIRE_IMG_RES, long-shift, lat-round(shift*1.5), self.fire_size, self.fire_size)

        def draw(self):
            self.draw_background()
            self.draw_fires()
            self.draw_aircrafts()

    def __init__(self, logging: bool = True, canvas_id: str = "gameview", unit_table_id: str = "unit", target_table_id: str = "target",
                 spec_sheet_id: str = "specsheet", game_state_id: str = "gamestate", game_time_id: str = "gametime",
                 score_modal_id: str = "scorePanelModal", score_panel_id: str = "score-panel-text",
                 api_log_id: str = "output", fos_version_info: str = "fos_version_info"):
        super().__init__(logging)
        self._elements = self.JSElements(canvas_id, unit_table_id, target_table_id,
                                         spec_sheet_id, game_state_id, game_time_id,
                                         score_modal_id, score_panel_id,
                                         api_log_id, fos_version_info)

        self._game_state = self.GameState.UNKNOWN
        self._round = 0

    async def set_game_round(self, new_round: int):
        """ Set Game Round """
        self._round = new_round
        logging.info(f"------- Round {new_round} is now started -------<br><br>")
        await self.set_game_state(self._game_state)

    def get_game_state(self): return self._game_state

    async def set_game_state(self, new_state: GameState):
        """ Set Game State. """
        self._game_state = new_state
        self._elements.set_game_state(new_state.to_str(self._round))

    async def set_round_mode(self, round_num: int, unit_table, target_list):
        """ Set Round Mode
        Internally, this function do initialization job for the object coordinates
        """
        await super().set_round_mode(round_num, unit_table, target_list)
        await self.set_game_round(round_num)
        await self.set_game_state(self.GameState.RUNNING)

    async def show_score_panel(self, round_num: int, is_win: bool, score: int):
        """ Show Score Panel when a round is finished """
        await super().show_score_panel(round_num, is_win, score)
        await self.set_game_state(self.GameState.END)
        self._elements.append_current_round_score(round_num, is_win, score)
        self._elements.launch_score_panel()

    async def _update_fire_state(self, target_list):
        """ Fire Status Update """
        self._elements.set_target_status(target_list)
        self._elements.update_target_table(target_list)

    async def _update_unit_status(self, unit_table, positions: dict[str, tuple[int, int]]):
        """ Update Game Play Screen """
        self._elements.set_aircraft_positions(positions)
        self._elements.update_unit_table(unit_table)

    async def _update_play_time(self, current_time: str):
        """ Update Game Play Time on the Screen """
        self._elements.set_game_time(current_time)

    async def add_order_log(self, order_xml: str, current_time: str):
        """ Update Order Status Log Sheet """
        await super().add_order_log(order_xml, current_time)
        self._elements.append_order_log(order_xml, current_time)

    async def _display_update(self):
        """ Refresh/Update Screen """
        self._elements.draw()


class CustomLogHandler(logging.Handler):
    def __init__(self, output_element: js.HTMLElement):
        super().__init__()
        self.output_element = output_element

    def emit(self, record: logging.LogRecord):
        text = self.format(record)
        log_level = record.levelname
        if log_level == "DEBUG":
            color = "white"
        elif log_level == "INFO":
            color = "white"
        elif log_level == "WARNING":
            color = "orange"
        elif log_level == "ERROR":
            color = "darkred"  # dark red

        self.output_element.prepend(js.document.createElement("br"))  # type: ignore
        self.output_element.prepend(js.document.createElement("span"))
        self.output_element.firstChild.innerHTML = text  # type: ignore
        self.output_element.firstChild.style.color = color  # type: ignore

    def flush(self):
        pass
