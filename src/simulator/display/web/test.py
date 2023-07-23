from logging import LogRecord
import js
import sys
import asyncio
from enum import Enum
import logging


class TargetPosition(Enum):
    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4
    T5 = 5
    T6 = 6
    T7 = 7
    T8 = 8
    T9 = 9

    def __str__(self) -> str:
        return 'T' + str(self.value)


class AircraftKind(Enum):
    AIRPLANE = 0
    HELICOPTER = 1
    DRONE = 2

    def __str__(self) -> str:
        if self == AircraftKind.AIRPLANE:
            return 'Airplane'
        elif self == AircraftKind.HELICOPTER:
            return 'Helicopter'
        elif self == AircraftKind.DRONE:
            return 'Drone'
        else:
            return 'Unknown Aircraft'


class AircraftModel(Enum):
    D1 = 0
    D2 = 1
    D3 = 2
    D4 = 3
    D5 = 4
    H1 = 5
    H2 = 6
    H3 = 7
    H4 = 8
    H5 = 9
    A1 = 10
    A2 = 11
    A3 = 12
    A4 = 13
    A5 = 14

    def to_aircraftKind(self) -> AircraftKind:
        if self.value < 5:
            return AircraftKind.DRONE
        elif self.value < 10:
            return AircraftKind.HELICOPTER
        else:
            return AircraftKind.AIRPLANE

    def __str__(self) -> str:
        if self == AircraftModel.D1:
            return 'D1'
        elif self == AircraftModel.D2:
            return 'D2'
        elif self == AircraftModel.D3:
            return 'D3'
        elif self == AircraftModel.D4:
            return 'D4'
        elif self == AircraftModel.D5:
            return 'D5'
        elif self == AircraftModel.H1:
            return 'H1'
        elif self == AircraftModel.H2:
            return 'H2'
        elif self == AircraftModel.H3:
            return 'H3'
        elif self == AircraftModel.H4:
            return 'H4'
        elif self == AircraftModel.H5:
            return 'H5'
        elif self == AircraftModel.A1:
            return 'A1'
        elif self == AircraftModel.A2:
            return 'A2'
        elif self == AircraftModel.A3:
            return 'A3'
        elif self == AircraftModel.A4:
            return 'A4'
        elif self == AircraftModel.A5:
            return 'A5'
        else:
            return 'Unknown Aircraft Model'


TARGET_LOCATIONS = {
    TargetPosition.T1: (280, 20),
    TargetPosition.T2: (280, 60),
    TargetPosition.T3: (280, 100),
    TargetPosition.T4: (240, 20),
    TargetPosition.T5: (240, 60),
    TargetPosition.T6: (240, 100),
    TargetPosition.T7: (200, 20),
    TargetPosition.T8: (200, 60),
    TargetPosition.T9: (200, 100)
}

AIRCRAFT_SOURCES = {
    AircraftModel.D1: 'drone1.png',
    AircraftModel.D2: 'drone2.png',
    AircraftModel.D3: 'drone3.png',
    AircraftModel.D4: 'drone4.png',
    AircraftModel.D5: 'drone5.png',
    AircraftModel.H1: 'heli1.png',
    AircraftModel.H2: 'heli2.png',
    AircraftModel.H3: 'heli3.png',
    AircraftModel.H4: 'heli4.png',
    AircraftModel.H5: 'heli5.png',
    AircraftModel.A1: 'plane1.png',
    AircraftModel.A2: 'plane2.png',
    AircraftModel.A3: 'plane3.png',
    AircraftModel.A4: 'plane4.png',
    AircraftModel.A5: 'plane5.png'
}

BACKGROUND_IMG_SOURCE = 'FOS_BACKGROUND.png'
FIRE_IMG_SOURCE = 'Fire1.png'
CANVAS_ID = 'gameview'
LOG_DIV_ID = 'output'
RESOURCE_PATH = 'res/'


class GameState(Enum):
    RUNNING = 0
    END = 1
    ERROR = 2
    PAUSE = 3
    UNKNOWN = 4


class Time(object):
    def __init__(self, hour: int, minute: int):
        if hour < 0 or hour > 23:
            raise ValueError('hour must be between 0 and 23')
        if minute < 0 or minute > 59:
            raise ValueError('minute must be between 0 and 59')
        self.hour = hour
        self.minute = minute

    def __str__(self) -> str:
        return '%02d:%02d' % (self.hour, self.minute)


class TargetType(Enum):
    FIRE = 0
    POSSIBLE_FIRE = 1
    NONE = 2

    def __str__(self) -> str:
        if self == TargetType.FIRE:
            return 'Fire'
        elif self == TargetType.POSSIBLE_FIRE:
            return 'Possible Fire'
        elif self == TargetType.NONE:
            return 'None'
        else:
            return 'Unknown Target Type'


class Round(Enum):
    ROUND1 = 'Round 1'
    ROUND2 = 'Round 2'
    ROUND3 = 'Round 3'

    def __str__(self) -> str:
        return self.value


class AB(Enum):
    A = "A"
    B = "B"

    def __str__(self) -> str:
        return self.value


class AircraftId(object):
    def __init__(self, aircraftModel: AircraftModel, ab: AB):
        self.aircraftModel = aircraftModel
        self.ab = ab

    def __str__(self) -> str:
        return str(self.aircraftModel) + "-" + str(self.ab)


class Aircraft(object):
    def __init__(self, aircraftID: AircraftId, x: int, y: int):
        self.aircraftID = aircraftID
        self.x = x
        self.y = y


class Spec(object):
    def __init__(self, aircraftModel: AircraftModel, veocity: int, timetoready: int, cost: int, area: int, timefilling: int, probability: int):
        self.aircraftModel = aircraftModel
        self.aircraft = aircraftModel.to_aircraftKind()
        self.veocity = veocity
        self.timetoready = timetoready
        self.cost = cost
        self.area = area
        self.timefilling = timefilling
        self.probability = probability

    def insert_to_table(self, table: js.HTMLTableElement):
        row: js.HTMLTableRowElement = table.insertRow()
        row.setAttribute('id', str(self.aircraftModel))  # type: ignore
        self.insert_to_row(row)

    def insert_to_row(self, row: js.HTMLTableRowElement):
        row.insertCell().innerHTML = str(self.aircraftModel)
        row.insertCell().innerHTML = str(self.aircraft)
        row.insertCell().innerHTML = str(self.veocity)
        row.insertCell().innerHTML = str(self.timetoready)
        row.insertCell().innerHTML = str(self.cost)
        row.insertCell().innerHTML = str(self.area)
        row.insertCell().innerHTML = str(self.timefilling)
        row.insertCell().innerHTML = str(self.probability)

    def __str__(self):
        return 'Spec(id=%s, aircraft=%s, veocity=%s, timetoready=%s, cost=%s, area=%s, timefilling=%s, probability=%s)' % (
            self.aircraftModel, self.aircraft, self.veocity, self.timetoready, self.cost, self.area, self.timefilling, self.probability
        )


class Target(object):
    def __init__(self, targeted: bool, targetposition: TargetPosition, priority: int, latitude: int, longitude: int, typeoftarget: TargetType, threat: str, probability: int):
        self.targeted = targeted
        self.name = targetposition
        self.priority = priority
        self.latitude = latitude
        self.longitude = longitude
        self.typeoftarget = typeoftarget
        self.threat = threat
        self.probability = probability

    def insert_to_table(self, table: js.HTMLTableElement):
        row = table.insertRow()
        row.setAttribute('id', str(self.name))  # type: ignore
        self.insert_to_row(row)

    def insert_to_row(self, row: js.HTMLTableRowElement):
        row.insertCell().innerHTML = str(self.targeted)
        row.insertCell().innerHTML = str(self.name)
        row.insertCell().innerHTML = str(self.priority)
        row.insertCell().innerHTML = str(self.latitude)
        row.insertCell().innerHTML = str(self.longitude)
        row.insertCell().innerHTML = str(self.typeoftarget)
        row.insertCell().innerHTML = self.threat
        row.insertCell().innerHTML = str(self.probability)

    def __str__(self):
        return 'Target(targeted=%s, name=%s, priority=%s, latitude=%s, longitude=%s, typeoftarget=%s, threat=%s, probability=%s)' % (
            self.targeted, self.name, self.priority, self.latitude, self.longitude, self.typeoftarget, self.threat, self.probability
        )


class Unit(object):
    def __init__(self, ordered: bool, available: bool, timeofreturn: Time, deparaturetime: Time, arrivaltime: Time, base: str, aircraft: AircraftId, waterlevel: int):
        self.ordered = ordered
        self.available = available
        self.timeofreturn = timeofreturn
        self.deparaturetime = deparaturetime
        self.arrivaltime = arrivaltime
        self.base = base
        self.aircraft = aircraft
        self.waterlevel = waterlevel

    def insert_to_table(self, table: js.HTMLTableElement):
        row = table.insertRow()
        row.setAttribute('id', str(self.aircraft))  # type: ignore
        self.insert_to_row(row)

    def insert_to_row(self, row: js.HTMLTableRowElement):
        row.insertCell().innerHTML = str(self.ordered)
        row.insertCell().innerHTML = str(self.available)
        row.insertCell().innerHTML = str(self.timeofreturn)
        row.insertCell().innerHTML = str(self.deparaturetime)
        row.insertCell().innerHTML = str(self.arrivaltime)
        row.insertCell().innerHTML = self.base
        row.insertCell().innerHTML = str(self.aircraft)
        row.insertCell().innerHTML = str(self.waterlevel)

    def __str__(self) -> str:
        return 'Unit(ordered=%s, available=%s, timeofreturn=%s, deparaturetime=%s, arrivaltime=%s, base=%s, aircraftid=%s, waterlevel=%s)' % (
            self.ordered, self.available, self.timeofreturn, self.deparaturetime, self.arrivaltime, self.base, self.aircraft, self.waterlevel
        )


def get_gamestate_text(gamestate: GameState, round: Round) -> str:
    if gamestate == GameState.RUNNING:
        return '🟢 %s Running' % round
    elif gamestate == GameState.END:
        return '🔴 %s End' % round
    elif gamestate == GameState.ERROR:
        return '🟠 %s Error' % round
    elif gamestate == GameState.PAUSE:
        return '🟡 %s Pause' % round
    else:
        return '⚪ %s Unknown' % round


async def load_image(route: str):
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    img: js.HTMLImageElement = js.Image.new()  # type: ignore

    def on_load(_):
        logging.info('filename: %s loaded' % route)
        if not future.done():
            future.set_result(img)

    def timeout():
        if not future.done():
            logging.error('filename: %s load timeout' % route)
            future.set_result(None)

    img.onload = on_load
    # set timeout of 5 seconds
    loop.call_later(0.1, timeout)

    img.src = RESOURCE_PATH + route

    return await future


class CustomLogHandler(logging.Handler):

    def __init__(self, output_element: js.HTMLElement):
        super().__init__()
        self.output_element = output_element

    def emit(self, record: logging.LogRecord):
        text = self.format(record)
        log_level = record.levelname
        if log_level == 'DEBUG':
            color = 'white'
        elif log_level == 'INFO':
            color = 'white'
        elif log_level == 'WARNING':
            color = 'orange'
        elif log_level == 'ERROR':
            color = 'darkred'

        self.output_element.appendChild(js.document.createElement('span'))
        self.output_element.lastChild.innerHTML = text # type: ignore
        self.output_element.lastChild.style.color = color  # type: ignore
        self.output_element.appendChild(js.document.createElement('br'))  # type: ignore

    def flush(self):
        pass


class GameVisualizer(object):
    def __init__(self) -> None:
        pass

    async def initialize(self):
        def backgroundOnLoad(_):
            logging.info('filename: %s loaded' % self.background)

        self.airplanes: dict[AircraftId, Aircraft] = {}
        self.fires: set[TargetPosition] = set()
        self.canvas: js.CanvasRenderingContext2D = js.document.getElementById(
            CANVAS_ID).getContext('2d')  # type: ignore
        self.unit: js.HTMLTableElement = js.document.getElementById(
            'unit')  # type: ignore
        self.target: js.HTMLTableElement = js.document.getElementById(
            'target')  # type: ignore
        self.specsheet: js.HTMLTableElement = js.document.getElementById(
            'specsheet')  # type: ignore
        self.background = BACKGROUND_IMG_SOURCE
        self.background_img: js.HTMLImageElement = js.Image.new()  # type: ignore
        self.background_img.src = RESOURCE_PATH + self.background
        self.background_img.onload = backgroundOnLoad
        aircraft_img_poll = {x.value: load_image(
            AIRCRAFT_SOURCES[x]) for x in AircraftModel}
        self.fire_img = await load_image(FIRE_IMG_SOURCE)
        self.aircraft_img = {AircraftModel(i): img for i, img in enumerate(await asyncio.gather(*aircraft_img_poll.values()))}
        self.canvas.drawImage(self.background_img, 0, 0)  # type: ignore
        self.gameStateText: js.HTMLElement = js.document.getElementById(
            'gamestate')  # type: ignore
        self.round: Round = Round.ROUND1
        self.gameState: GameState = GameState.UNKNOWN
        self.gameStateText.innerHTML = get_gamestate_text(  # type: ignore
            self.round, self.gameState)  # type: ignore
        self.specs: dict[AircraftModel, Spec] = {}
        self.targets: dict[TargetPosition, Target] = {}
        self.units: dict[AircraftId, Unit] = {}

    def insert_spec(self, spec: Spec):
        self.specs[spec.aircraftModel] = spec
        spec.insert_to_table(self.specsheet)

    def update_spec(self, aircraftModel: AircraftModel, spec: Spec):
        assert (aircraftModel in self.specs.keys()
                ), 'aircraftid: %s not found' % aircraftModel
        assert (spec.aircraftModel ==
                aircraftModel), 'aircraftid: %s not match' % aircraftModel
        row: js.HTMLTableRowElement = js.document.getElementById(
            str(aircraftModel))  # type: ignore
        for _ in range(8):
            row.deleteCell(0)  # type: ignore
        spec.insert_to_row(row)

    def delete_spec(self, aircraftModel: AircraftModel):
        assert (aircraftModel in self.specs.keys()
                ), 'aircraftid: %s not found' % aircraftModel
        row = js.document.getElementById(str(aircraftModel))
        row.parentElement.removeChild(row)  # type: ignore
        self.specs.pop(aircraftModel)

    def insert_target(self, target: Target):
        self.targets[target.name] = target
        target.insert_to_table(self.target)  # type: ignore

    def update_target(self, targetposition: TargetPosition, target: Target):
        assert targetposition in self.targets.keys(
        ), 'targetposition: %s not found' % targetposition
        assert target.name == targetposition, 'target.name: %s != targetposition: %s' % (
            target.name, targetposition)
        row = js.document.getElementById(str(targetposition))
        for _ in range(8):
            row.deleteCell(0)  # type: ignore
        target.insert_to_row(row)  # type: ignore

    def delete_target(self, targetposition: TargetPosition):
        assert targetposition in self.targets.keys(
        ), 'targetposition: %s not found' % targetposition
        row: js.HTMLTableRowElement = js.document.getElementById(
            str(targetposition))  # type: ignore
        row.parentElement.removeChild(row)  # type: ignore
        self.targets.pop(targetposition)

    def insert_unit(self, unit: Unit):
        self.units[unit.aircraft] = unit
        unit.insert_to_table(self.unit)

    def update_unit(self, aircraftId: AircraftId, unit: Unit):
        assert (aircraftId in self.units.keys()
                ), 'aircraftId: %s not found' % aircraftId
        row: js.HTMLTableRowElement = js.document.getElementById(
            str(aircraftId))  # type: ignore
        for _ in range(8):
            row.deleteCell(0)  # type: ignore
        unit.insert_to_row(row)  # type: ignore

    def delete_unit(self, aircraftId: AircraftId):
        assert (aircraftId in self.units.keys()
                ), 'aircraftId: %s not found' % aircraftId
        row = js.document.getElementById(str(aircraftId))
        row.parentElement.removeChild(row)  # type: ignore
        self.units.pop(aircraftId)

    def spawn_airplane(self, x: int, y: int, aircraftId: AircraftId):
        airplane: Aircraft = Aircraft(aircraftId, x, y)
        # check if the aircraft type is already in the set
        self.airplanes[aircraftId] = airplane

    def update_airplane(self, x: int, y: int, aircraftId: AircraftId):
        self.airplanes[aircraftId].x = x
        self.airplanes[aircraftId].y = y

    def despawn_airplane(self, aircraftId: AircraftId):
        self.airplanes.pop(aircraftId)

    def spawn_fire(self, target: TargetPosition):
        self.fires.add(target)

    def despawn_fire(self, target: TargetPosition):
        self.fires.remove(target)

    def draw_background(self):
        self.canvas.drawImage(self.background_img, 0, 0)  # type: ignore

    def draw_aircrafts(self):
        for airplane in self.airplanes.values():
            self.canvas.drawImage(  # type: ignore
                self.aircraft_img[airplane.aircraftID.aircraftModel], airplane.x - 25, airplane.y - 25, 50, 50)

    def draw_fires(self):
        for target in self.fires:
            self.canvas.drawImage(  # type: ignore
                self.fire_img, TARGET_LOCATIONS[target][0] - 25, TARGET_LOCATIONS[target][1] - 25, 50, 50)

    def draw(self):
        self.draw_background()
        self.draw_aircrafts()
        self.draw_fires()

    def set_round(self, round: Round):
        self.round = round
        self.gameStateText.innerHTML = get_gamestate_text(
            self.gameState, self.round)

    def set_gamestate(self, gamestate: GameState):
        self.gameState = gamestate
        self.gameStateText.innerHTML = get_gamestate_text(
            self.gameState, self.round)


async def stop():
    logging.info('stop')


async def start():
    logging.info('start')


async def reset():
    logging.info('reset')


async def main():
    format = "%(asctime)s [%(levelname)s] %(message)s"

    logging.basicConfig(handlers=[CustomLogHandler(
        js.document.getElementById(LOG_DIV_ID))], level=logging.INFO, format=format) # type: ignore

    visualizer = GameVisualizer()
    await visualizer.initialize()

    visualizer.set_gamestate(GameState.RUNNING)
    visualizer.set_round(Round.ROUND1)

    plane1 = AircraftId(AircraftModel.A1, AB.A)
    plane2 = AircraftId(AircraftModel.A1, AB.B)
    plane3 = AircraftId(AircraftModel.D1, AB.A)

    visualizer.spawn_airplane(200, 200, plane1)
    visualizer.draw()

    visualizer.spawn_airplane(100, 100, plane2)
    visualizer.draw()

    visualizer.spawn_airplane(100, 200, plane3)
    visualizer.draw()

    visualizer.spawn_fire(TargetPosition.T4)
    visualizer.draw()

    async def animation():
        forward = True
        while True:
            await asyncio.sleep(1/60)
            if forward:
                visualizer.update_airplane(
                    visualizer.airplanes[plane3].x + 4, visualizer.airplanes[plane3].y, plane3)
            else:
                visualizer.update_airplane(
                    visualizer.airplanes[plane3].x - 4, visualizer.airplanes[plane3].y, plane3)
            if visualizer.airplanes[plane3].x > 300:
                forward = False
            elif visualizer.airplanes[plane3].x < 100:
                forward = True
            visualizer.draw()

    asyncio.create_task(animation())
    spec1 = Spec(AircraftModel.A1, 100, 100, 100, 100, 100, 100)
    spec2 = Spec(AircraftModel.D5, 100, 100, 100, 100, 100, 100)
    target1 = Target(False, TargetPosition.T1, 100, 100,
                     100, TargetType.FIRE, "threat1", 100)
    target2 = Target(True, TargetPosition.T2, 100, 100,
                     100, TargetType.NONE, "threat2", 100)
    unit1 = Unit(True, False, Time(10, 10), Time(
        10, 10), Time(10, 10), "base1", plane1, 100)
    unit2 = Unit(False, True, Time(10, 10), Time(
        10, 10), Time(10, 10), "base2", plane2, 100)
    visualizer.insert_spec(spec1)
    visualizer.insert_spec(spec2)
    visualizer.insert_target(target1)
    visualizer.insert_target(target2)
    visualizer.insert_unit(unit1)
    visualizer.insert_unit(unit2)

    await asyncio.sleep(1)
    spec3 = Spec(AircraftModel.A1, 100, 200, 200, 200, 200, 200)
    visualizer.update_spec(AircraftModel.A1, spec3)
    visualizer.delete_spec(AircraftModel.D5)
    target3 = Target(False, TargetPosition.T2, 100, 100,
                     100, TargetType.FIRE, "threat3", 100)
    visualizer.update_target(TargetPosition.T2, target3)
    visualizer.delete_target(TargetPosition.T1)
    unit3 = Unit(True, False, Time(10, 10), Time(
        10, 10), Time(10, 10), "base3", plane2, 100)
    visualizer.update_unit(plane2, unit3)
    visualizer.delete_unit(plane1)

    js.console.log(type(js.document.getElementById('specsheet'))) # type: ignore

    logging.warning("test warning")
    logging.error("test error")
    logging.debug("test debug")
    logging.info("test info")

    await asyncio.sleep(1)
    visualizer.set_gamestate(GameState.END)
