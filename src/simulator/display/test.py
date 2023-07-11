import js
import sys, asyncio
from enum import Enum


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

class Round(Enum):
    ROUND1 = 0
    ROUND2 = 1
    ROUND3 = 2

    def __str__(self) -> str:
        if self == Round.ROUND1:
            return 'Round 1'
        elif self == Round.ROUND2:
            return 'Round 2'
        elif self == Round.ROUND3:
            return 'Round 3'
        else:
            return 'Unknown Round'

class Spec(object):
    def __init__(self, aircraftid, aircraft, veocity, timetoready, cost, area, timefilling, probability):
        self.aircraftid = aircraftid
        self.aircraft = aircraft
        self.veocity = veocity
        self.timetoready = timetoready
        self.cost = cost
        self.area = area
        self.timefilling = timefilling
        self.probability = probability
    
    def insert_to_table(self, table):
        row = table.insertRow()
        row.setAttribute('id', self.aircraftid)
        self.insert_to_row(row)

    def insert_to_row(self, row):
        row.insertCell().innerHTML = self.aircraftid
        row.insertCell().innerHTML = self.aircraft
        row.insertCell().innerHTML = self.veocity
        row.insertCell().innerHTML = self.timetoready
        row.insertCell().innerHTML = self.cost
        row.insertCell().innerHTML = self.area
        row.insertCell().innerHTML = self.timefilling
        row.insertCell().innerHTML = self.probability

    def __str__(self):
        return 'Spec(id=%s, aircraft=%s, veocity=%s, timetoready=%s, cost=%s, area=%s, timefilling=%s, probability=%s)' % (
            self.aircraftid, self.aircraft, self.veocity, self.timetoready, self.cost, self.area, self.timefilling, self.probability
        )
    
class Target(object):
    def __init__(self, targeted, name, priority, latitude, longitude, typeoftarget, threat, probability):
        self.targeted = targeted
        self.name = name
        self.priority = priority
        self.latitude = latitude
        self.longitude = longitude
        self.typeoftarget = typeoftarget
        self.threat = threat
        self.probability = probability
    
    def insert_to_table(self, table):
        row = table.insertRow()
        row.setAttribute('id', self.name)
        self.insert_to_row(row)

    def insert_to_row(self, row):
        row.insertCell().innerHTML = self.targeted
        row.insertCell().innerHTML = self.name
        row.insertCell().innerHTML = self.priority
        row.insertCell().innerHTML = self.latitude
        row.insertCell().innerHTML = self.longitude
        row.insertCell().innerHTML = self.typeoftarget
        row.insertCell().innerHTML = self.threat
        row.insertCell().innerHTML = self.probability

    def __str__(self):
        return 'Target(targeted=%s, name=%s, priority=%s, latitude=%s, longitude=%s, typeoftarget=%s, threat=%s, probability=%s)' % (
            self.targeted, self.name, self.priority, self.latitude, self.longitude, self.typeoftarget, self.threat, self.probability
        )
    
class Unit(object):
    def __init__(self, ordered, available, timeofreturn, deparaturetime, arrivaltime, base, aircraftid, waterlevel):
        self.ordered = ordered
        self.available = available
        self.timeofreturn = timeofreturn
        self.deparaturetime = deparaturetime
        self.arrivaltime = arrivaltime
        self.base = base
        self.aircraftid = aircraftid
        self.waterlevel = waterlevel

    def insert_to_table(self, table):
        row = table.insertRow()
        row.setAttribute('id', self.aircraftid)
        self.insert_to_row(row)

    def insert_to_row(self, row):
        row.insertCell().innerHTML = self.ordered
        row.insertCell().innerHTML = self.available
        row.insertCell().innerHTML = self.timeofreturn
        row.insertCell().innerHTML = self.deparaturetime
        row.insertCell().innerHTML = self.arrivaltime
        row.insertCell().innerHTML = self.base
        row.insertCell().innerHTML = self.aircraftid
        row.insertCell().innerHTML = self.waterlevel

    def __str__(self):
        return 'Unit(ordered=%s, available=%s, timeofreturn=%s, deparaturetime=%s, arrivaltime=%s, base=%s, aircraftid=%s, waterlevel=%s)' % (
            self.ordered, self.available, self.timeofreturn, self.deparaturetime, self.arrivaltime, self.base, self.aircraftid, self.waterlevel
        )

def get_round_text(round):
    if round == Round.ROUND1:
        return 'Round 1'
    elif round == Round.ROUND2:
        return 'Round 2'
    elif round == Round.ROUND3:
        return 'Round 3'
    else:
        return 'Unknown Round'

def get_gamestate_text(gamestate, round):
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

class TargetPosition(Enum):
    T1 = 0
    T2 = 1
    T3 = 2
    T4 = 3
    T5 = 4
    T6 = 5
    T7 = 6
    T8 = 7
    T9 = 8

class AircraftKind(Enum):
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
    AircraftKind.D1: 'drone1.png',
    AircraftKind.D2: 'drone2.png',
    AircraftKind.D3: 'drone3.png',
    AircraftKind.D4: 'drone4.png',
    AircraftKind.D5: 'drone5.png',
    AircraftKind.H1: 'heli1.png',
    AircraftKind.H2: 'heli2.png',
    AircraftKind.H3: 'heli3.png',
    AircraftKind.H4: 'heli4.png',
    AircraftKind.H5: 'heli5.png',
    AircraftKind.A1: 'plane1.png',
    AircraftKind.A2: 'plane2.png',
    AircraftKind.A3: 'plane3.png',
    AircraftKind.A4: 'plane4.png',
    AircraftKind.A5: 'plane5.png'
}

async def load_image(route):
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    img = js.Image.new()

    def on_load(_):
        print('[INFO] filename: %s loaded' % route)
        if not future.done():
            future.set_result(img)

    def timeout():
        if not future.done():
            print('[ERROR] filename: %s load timeout' % route)
            future.set_result(None)

    img.onload = on_load
    # set timeout of 5 seconds
    loop.call_later(0.1, timeout)

    img.src = RESOURCE_PATH + route

    return await future

class Logger():
    def __init__(self, output_element):
        self.output_element = output_element
    
    def write(self, text):
        text = text.replace('\n', '<br>')
        self.output_element.innerHTML += text
    
    def flush(self):
        pass

class AirCraft(object):
    def __init__(self, x, y, aircraftkind):
        self.x = x
        self.y = y
        self.Aircraft = aircraftkind

class GameVisualizer(object):
    def __init__(self) -> None:
        pass

    async def initialize(self):
        self.airplanes: dict[str, AirCraft] = {}
        self.fires: set[TargetPosition] = set()
        self.canvas = js.document.getElementById(CANVAS_ID).getContext('2d')
        print(self.canvas)
        self.unit = js.document.getElementById('unit')
        self.target = js.document.getElementById('target')
        self.specsheet = js.document.getElementById('specsheet')
        self.background = BACKGROUND_IMG_SOURCE
        self.background_img = js.Image.new()
        self.background_img.src = RESOURCE_PATH + self.background
        self.background_img.onload = lambda x: print('[INFO] filename: %s loaded' % self.background)
        aircraft_img_poll = {x.value: load_image(AIRCRAFT_SOURCES[x]) for x in AircraftKind}
        self.fire_img = await load_image(FIRE_IMG_SOURCE)
        self.aircraft_img = {AircraftKind(i) : img for i, img in enumerate(await asyncio.gather(*aircraft_img_poll.values()))}
        self.canvas.drawImage(self.background_img, 0, 0)
        self.gamestate = js.document.getElementById('gamestate')
        self.round = Round.ROUND1
        self.gameState = GameState.UNKNOWN
        self.gamestate.innerHTML = get_gamestate_text(self.round, self.gameState)
        self.specs : dict[str, Spec] = {};
        self.targets : dict[str, Target] = {};
        self.units : dict[str, Unit] = {};
    
    def spawn_airplane(self, x, y, aircraft, id):
        airplane: AirCraft = AirCraft(x, y, aircraft)
        # check if the aircraft type is already in the set
        self.airplanes[id] = airplane

    def insert_spec(self, spec: Spec):
        self.specs[spec.aircraftid] = spec
        spec.insert_to_table(self.specsheet)

    def update_spec(self, aircraftid, spec: Spec):
        if aircraftid not in self.specs.keys():
            print('[ERROR] aircraftid: %s not found' % aircraftid)
        row = js.document.getElementById(aircraftid)
        for i in range(8): row.deleteCell(0)
        spec.insert_to_row(row)

    def delete_spec(self, aircraftid):
        if aircraftid not in self.specs.keys():
            print('[ERROR] aircraftid: %s not found' % aircraftid)
        row = js.document.getElementById(aircraftid)
        row.parentElement.removeChild(row)
        self.specs.pop(aircraftid)

    def insert_target(self, target: Target):
        self.targets[target.name] = target
        target.insert_to_table(self.target)

    def update_target(self, targetid, target: Target):
        if targetid not in self.targets.keys():
            print('[ERROR] targetid: %s not found' % targetid)
        row = js.document.getElementById(targetid)
        for i in range(8): row.deleteCell(0)
        target.insert_to_row(row)

    def delete_target(self, targetid):
        if targetid not in self.targets.keys():
            print('[ERROR] targetid: %s not found' % targetid)
        row = js.document.getElementById(targetid)
        row.parentElement.removeChild(row)
        self.targets.pop(targetid)

    def insert_unit(self, unit: Unit):
        self.units[unit.aircraftid] = unit
        unit.insert_to_table(self.unit)

    def update_unit(self, unitid, unit: Unit):
        if unitid not in self.units.keys():
            print('[ERROR] unitid: %s not found' % unitid)
        row = js.document.getElementById(unitid)
        for i in range(8): row.deleteCell(0)
        unit.insert_to_row(row)

    def delete_unit(self, unitid):
        if unitid not in self.units.keys():
            print('[ERROR] unitid: %s not found' % unitid)
        row = js.document.getElementById(unitid)
        row.parentElement.removeChild(row)
        self.units.pop(unitid)
    
    def update_airplane(self, x, y, id):
        self.airplanes[id].x = x
        self.airplanes[id].y = y

    def despawn_airplane(self, id):
        self.airplanes.pop(id)
    
    def spawn_fire(self, target):
        self.fires.add(target)

    def despawn_fire(self, target):
        self.fires.remove(target)
    
    def draw_background(self):
        self.canvas.drawImage(self.background_img, 0, 0)

    def draw_aircrafts(self):
        for airplane in self.airplanes.values():
            self.canvas.drawImage(self.aircraft_img[airplane.Aircraft], airplane.x - 25, airplane.y - 25, 50, 50)
            

    def draw_fires(self):
        for target in self.fires:
            self.canvas.drawImage(self.fire_img, TARGET_LOCATIONS[target][0] - 25, TARGET_LOCATIONS[target][1] - 25, 50, 50)

    def draw(self):
        self.draw_background()
        self.draw_aircrafts()
        self.draw_fires()

    def set_round(self, round: Round):
        self.round = round
        self.gamestate.innerHTML = get_gamestate_text(self.gameState, self.round)

    def set_gamestate(self, gamestate: GameState):
        self.gameState = gamestate
        self.gamestate.innerHTML = get_gamestate_text(self.gameState, self.round)



async def stop():
    print('[INFO] stop')

async def start():
    print('[INFO] start')

async def reset():
    print('[INFO] reset')


    
async def main():
    sys.stdout = Logger(js.document.getElementById(LOG_DIV_ID))

    visualizer = GameVisualizer()
    await visualizer.initialize()

    visualizer.set_gamestate(GameState.RUNNING)
    visualizer.set_round(Round.ROUND1)

    visualizer.spawn_airplane(200, 200, AircraftKind.D1, '1')
    visualizer.draw()

    visualizer.spawn_airplane(100, 100, AircraftKind.H1, '2')
    visualizer.draw()

    visualizer.spawn_airplane(100, 100, AircraftKind.A1, '2')
    visualizer.draw()

    visualizer.spawn_fire(TargetPosition.T4)
    visualizer.draw()

    async def animation():
        forward = True
        while True:
            await asyncio.sleep(1/60)
            if forward:
                visualizer.update_airplane(visualizer.airplanes['1'].x + 4, visualizer.airplanes['1'].y, '1')
            else:
                visualizer.update_airplane(visualizer.airplanes['1'].x - 4, visualizer.airplanes['1'].y, '1')
            if visualizer.airplanes['1'].x > 300:
                forward = False
            elif visualizer.airplanes['1'].x < 100:
                forward = True
            visualizer.draw()
    
    asyncio.create_task(animation())


    print("Hello World")
    spec1 = Spec('D1', 'Drone', 100, 100, 100, 100, 100, 100)
    spec2 = Spec('H1', 'Heli', 100, 100, 100, 100, 100, 100)
    target1 = Target(100, 'T1', 100, 100, 100, 100, 100, 100)
    target2 = Target(100, 'T2', 100, 100, 100, 100, 100, 100)
    unit1 = Unit(100, 100, 100, 100, 100, 100, "D1-A", 100)
    unit2 = Unit(100, 100, 100, 100, 100, 100, "H1-B", 100)
    visualizer.insert_spec(spec1)
    visualizer.insert_spec(spec2)
    visualizer.insert_target(target1)
    visualizer.insert_target(target2)
    visualizer.insert_unit(unit1)
    visualizer.insert_unit(unit2)

    await asyncio.sleep(1)
    spec3 = Spec('H1', 'Heli', 200, 200, 100, 200, 200, 200)
    visualizer.update_spec('H1', spec3)
    visualizer.delete_spec('D1')
    target3 = Target(100, 'T2', 100, 100, 100, 100, 100, 100)
    visualizer.update_target('T2', target3)
    visualizer.delete_target('T1')
    unit3 = Unit(100, 100, 100, 100, 100, 100, "H1-B", 100)
    visualizer.update_unit('H1-B', unit3)
    visualizer.delete_unit('D1-A')

    js.console.log(type(js.document.getElementById('specsheet')))
    print("what?")

    await asyncio.sleep(1)
    visualizer.set_gamestate(GameState.END)
    