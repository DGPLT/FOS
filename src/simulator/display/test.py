import js
import sys, asyncio
from enum import Enum

BACKGROUND_IMG_SOURCE = 'FOS_BACKGROUND.png'
FIRE_IMG_SOURCE = 'Fire1.png'
CANVAS_ID = 'gameview'
LOG_DIV_ID = 'output'
RESOURCE_PATH = 'res/'

class Target(Enum):
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
    Target.T1: (280, 20),
    Target.T2: (280, 60),
    Target.T3: (280, 100),
    Target.T4: (240, 20),
    Target.T5: (240, 60),
    Target.T6: (240, 100),
    Target.T7: (200, 20),
    Target.T8: (200, 60),
    Target.T9: (200, 100)
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
        self.fires: set[Target] = set()
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
        
    
    def spawn_airplane(self, x, y, aircraft, id):
        airplane: AirCraft = AirCraft(x, y, aircraft)
        # check if the aircraft type is already in the set
        self.airplanes[id] = airplane

    def insert_row_specsheet(self, id, aircraft, veocity, timetoready, cost, area, timefilling, probability):
        row = self.specsheet.insertRow()
        row.id = id
        row.insertCell().innerHTML = id
        row.insertCell().innerHTML = aircraft
        row.insertCell().innerHTML = veocity
        row.insertCell().innerHTML = timetoready
        row.insertCell().innerHTML = cost
        row.insertCell().innerHTML = area
        row.insertCell().innerHTML = timefilling
        row.insertCell().innerHTML = probability

    
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


    
async def main():
    sys.stdout = Logger(js.document.getElementById(LOG_DIV_ID))

    visualizer = GameVisualizer()
    await visualizer.initialize()

    visualizer.spawn_airplane(200, 200, AircraftKind.D1, '1')
    visualizer.draw()

    visualizer.spawn_airplane(100, 100, AircraftKind.H1, '2')
    visualizer.draw()

    visualizer.spawn_airplane(100, 100, AircraftKind.A1, '2')
    visualizer.draw()

    visualizer.spawn_fire(Target.T4)
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

    visualizer.insert_row_specsheet('1', 'D1', 100, 100, 100, 100, 100, 100)
    visualizer.insert_row_specsheet('2', 'H1', 100, 100, 100, 100, 100, 100)


    