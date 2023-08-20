import asyncio
import json
import time
import pandas as pd


class WebConnectionBuilder:
    ENCODING = 'utf8'

    def __init__(self):
        super().__init__()
        import js as _js
        global js
        js = _js

    async def connect(self):
        print("trying to connect with webRTC...")
        js.rtcConnect()
        while not js.rtcConnected:
            await asyncio.sleep(0)
        print("webRTC channel connected!")

    async def send(self, msg):
        if type(msg) == bytes:
            msg = msg.decode(self.ENCODING)
        js.rtcDataChannel.send(msg)

    async def recv(self):
        while not js.rtcBuffer:
            await asyncio.sleep(0)
        msg = js.rtcBuffer
        js.rtcBuffFlush()
        if type(msg) == str:
            pass
        elif type(msg) == bytes:
            msg = msg.decode(self.ENCODING)
        else:  # pyodide.ffi.JsProxy -> memoryview -> str
            msg = str(msg.to_py(), self.ENCODING)
        print("RTC RECEIVED:", msg)
        return msg


async def main():
    rtc = WebConnectionBuilder()
    
    # client accept
    print("receiving client")
    while not js.rtcConnected:
        await asyncio.sleep(0)

    while True:
        msg = await rtc.recv()
        if msg == "!CONNECTED!":
            break
        await asyncio.sleep(0)

    # start
    print("/start")
    await rtc.send("/start")
    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)


    # data get
    print("/data/aircraft_specsheet")
    await rtc.send("/data/aircraft_specsheet")
    spec = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(spec)
    print(pd.DataFrame.from_dict(data=json.loads(spec[0]['data']), orient='index'))

    print("/data/target_list")
    await rtc.send("/data/target_list")
    targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(targets)
    print(pd.DataFrame.from_dict(data=json.loads(targets[0]['data']), orient='columns'))

    print("/data/unit_table")
    await rtc.send("/data/unit_table")
    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(units)
    print(pd.DataFrame.from_dict(data=json.loads(units[0]['data']), orient='index'))

    Target_dict = json.loads(targets[0]['data'])
    Target_dict
    Target_list_temp=[]
    random_target = 'T0'
    for i in range(1,10):
        random_target_temp = 'T'+f'{i}'
        if(Target_dict['Targets'][random_target_temp]['probability'] != 0):
            Target_list_temp.append(Target_dict['Targets'][random_target_temp])
            random_target = random_target_temp
    Lake_info = Target_dict['Lakes']['L1']

    #좌표 한칸당 1km로 가정
    import math
    import collections
    lake_lat = Lake_info['latitude']
    lake_long = Lake_info['longitude']

    base_list = ['A', 'B', 'C']
    base_lat = {}
    base_long = {}
    unit_dict = json.loads(units[0]['data'])
    aircraft_info = json.loads(spec[0]['data'])
    time_dict = {}
    weighted_cost = {}
    for i in base_list:
        base_lat[i] = Target_dict['Bases'][i]['latitude']
        base_long[i] = Target_dict['Bases'][i]['longitude']

    def select_aircraft(Target_list, round_num):
        result_aircraft = []
        for i in range(0, round_num):
            target_lat = Target_list[i]['latitude']
            target_long = Target_list[i]['longitude']

            for name in unit_dict:
                result_time = 0
                aircraft_name = name[0:2]
                velocity = aircraft_info[aircraft_name]['Velocity']
                base_name = unit_dict[name]['Base']
                water_need = 100 - unit_dict[name]['Current Water']
                water_fulltime = aircraft_info[aircraft_name]['Water Tank']
                Time_water = water_fulltime*(water_need/100)
                if(Time_water != 0):
                    result_time = aircraft_info[aircraft_name]['ETRDY'] +Time_water + (math.sqrt((lake_lat - base_lat[base_name])**2 + (lake_long - base_long[base_name])**2)/velocity)*60 + (math.sqrt((target_lat - lake_lat)**2 + (target_long - lake_long)**2)/velocity)*60
                else:
                    result_time = aircraft_info[aircraft_name]['ETRDY'] + (math.sqrt((target_lat - base_lat[base_name])**2 + (target_long - base_long[base_name])**2)/velocity)*60
                time_dict[name] = result_time
                weight = (100 / aircraft_info[aircraft_name]['Possibility'])**2

                weighted_cost[name] = int(((aircraft_info[aircraft_name]['Cost']*weight/90.0)**1.16 + 10*math.log10((result_time*weight+2)**2)) * 100)

            sorted_cost = sorted(weighted_cost.items(), key=lambda x: x[1], reverse=False)

            result_aircraft.append(sorted_cost)
        return result_aircraft


    xml = f'''<operations>
    <order>
        <time>0601</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,1)[0][0][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,1)[0][0][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,1)[0][0][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target}</course>
    </order>
    <order>
        <time>0602</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,1)[0][1][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,1)[0][1][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,1)[0][1][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target}</course>
    </order>
</operations>'''
    time.sleep(0.25)
    print("/order")
    await rtc.send(f"/order/{xml}")
    order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(order_result)

    await rtc.send(f"/data/unit_table")
    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(units)


    xml_skip = '''<operations>
            </operations>'''
    aircraft_number = 2
    while(True):
        check = 0
        trigger = 0
        time.sleep(0.25)
        await rtc.send(f"/order/{xml_skip}")

        order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        order_result

        await rtc.send("/data/target_list")

        targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        targets

        try:
            Target_dict = json.loads(targets[0]['data'])
            Target_dict
        except:
            break

        Target_list_temp=[]
        random_target = []

        for i in range(1,10):
            random_target_temp = 'T'+f'{i}'
            if(Target_dict['Targets'][random_target_temp]['threat'] == 0):
                check = check + 1

            if(Target_dict['Targets'][random_target_temp]['probability'] != 0 and Target_dict['Targets'][random_target_temp]['targeted'] != True):
                aircraft_number = aircraft_number + 1
                if (aircraft_number >= 30):
                    aircraft_number = aircraft_number % 30
                trigger = 1
                Target_list_temp.append(Target_dict['Targets'][random_target_temp])
                random_target.append(random_target_temp)
        if(check == 9):
            break
        if trigger == 1:
            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

            xml = \
f'''<operations>
    <order>
        <time>{"0"+str(int(units[0]['time'])+1)}</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,1)[0][aircraft_number][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,1)[0][aircraft_number][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,1)[0][aircraft_number][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
</operations>'''
            time.sleep(0.25)
            await rtc.send(f"/order/{xml}")

            order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            order_result

            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

    await rtc.send("/result")

    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)
    time.sleep(2)

    await rtc.send("/start")

    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(units)

    await rtc.send("/data/target_list")

    targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(targets)

    Target_list = pd.DataFrame.from_dict(data=json.loads(targets[0]['data']), orient='columns')

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(units)

    Target_dict = json.loads(targets[0]['data'])

    Target_list_temp=[]
    random_target = []
    for i in range(1,10):
        random_target_temp = 'T'+f'{i}'
        if(Target_dict['Targets'][random_target_temp]['probability'] != 0):
            Target_list_temp.append(Target_dict['Targets'][random_target_temp])
            random_target.append(random_target_temp)
    Lake_info = Target_dict['Lakes']['L1']

    lake_lat = Lake_info['latitude']
    lake_long = Lake_info['longitude']

    base_list = ['A', 'B', 'C']
    base_lat ={}
    base_long = {}
    unit_dict = json.loads(units[0]['data'])
    aircraft_info = json.loads(spec[0]['data'])
    time_dict = {}
    weighted_cost = {}
    for i in base_list:
        base_lat[i] = Target_dict['Bases'][i]['latitude']
        base_long[i] = Target_dict['Bases'][i]['longitude']

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    xml = \
f'''<operations>
    <order>
        <time>0601</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,2)[0][0][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,2)[0][0][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,2)[0][0][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
    <order>
        <time>0602</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,2)[0][1][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,2)[0][1][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,2)[0][1][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[1]}</course>
    </order>
    <order>
        <time>0603</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,2)[0][2][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,2)[0][2][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,2)[0][2][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
    <order>
        <time>0604</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,2)[0][3][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,2)[0][3][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,2)[0][3][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[1]}</course>
    </order>
</operations>'''

    time.sleep(0.25)
    await rtc.send(f"/order/{xml}")

    order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(order_result)

    xml_skip = '''<operations>
                </operations>'''

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    aircraft_number = 4
    iter_num_list = []
    while True:
        time.sleep(0.25)
        check = 0
        trigger = 0
        await rtc.send(f"/order/{xml_skip}")

        order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        order_result

        await rtc.send("/data/target_list")

        targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        targets

        try:
            Target_dict = json.loads(targets[0]['data'])
            Target_dict
        except:
            break

        Target_list_temp=[]
        random_target = []
        for i in range(1,10):
            random_target_temp = 'T'+f'{i}'
            if(Target_dict['Targets'][random_target_temp]['threat'] == 0):
                check = check + 1

            if(Target_dict['Targets'][random_target_temp]['probability'] != 0 and Target_dict['Targets'][random_target_temp]['targeted'] != True):
                aircraft_number = aircraft_number + 1
                if (aircraft_number >= 30):
                    aircraft_number = aircraft_number % 30
                trigger = 1
                Target_list_temp.append(Target_dict['Targets'][random_target_temp])
                random_target.append(random_target_temp)
        if(check == 9):
            break
        if trigger == 1:
            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

            xml = \
f'''<operations>
    <order>
        <time>{"0"+str(int(units[0]['time'])+1)}</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,1)[0][aircraft_number][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,1)[0][aircraft_number][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,1)[0][aircraft_number][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
</operations>'''
            
            time.sleep(0.25)
            await rtc.send(f"/order/{xml}")

            order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            order_result

            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

    await rtc.send("/result")

    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)
    time.sleep(2)

    await rtc.send("/start")

    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    await rtc.send("/data/target_list")

    targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    Target_list = pd.DataFrame.from_dict(data=json.loads(targets[0]['data']), orient='columns')

    Target_dict = json.loads(targets[0]['data'])
    Target_dict
    Target_list_temp=[]
    random_target = []
    for i in range(1,10):
        random_target_temp = 'T'+f'{i}'
        if(Target_dict['Targets'][random_target_temp]['probability'] != 0):
            Target_list_temp.append(Target_dict['Targets'][random_target_temp])
            random_target.append(random_target_temp)
    Lake_info = Target_dict['Lakes']['L1']

    lake_lat = Lake_info['latitude']
    lake_long = Lake_info['longitude']

    base_list = ['A', 'B', 'C']
    base_lat ={}
    base_long = {}
    unit_dict = json.loads(units[0]['data'])
    aircraft_info = json.loads(spec[0]['data'])
    time_dict = {}
    weighted_cost = {}
    for i in base_list:
        base_lat[i] = Target_dict['Bases'][i]['latitude']
        base_long[i] = Target_dict['Bases'][i]['longitude']

    xml = \
f'''<operations>
    <order>
        <time>0601</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][0][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][0][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][0][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
    <order>
        <time>0602</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][1][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][1][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][1][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[1]}</course>
    </order>
    <order>
        <time>0603</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][2][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][2][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][2][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[2]}</course>
    </order>
    <order>
        <time>0604</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][3][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][3][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][3][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
    <order>
        <time>0605</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][4][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][4][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][4][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[1]}</course>
    </order>
    <order>
        <time>0606</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,3)[0][5][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,3)[0][5][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,3)[0][5][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[2]}</course>
    </order>
</operations>'''
    
    time.sleep(0.25)
    await rtc.send(f"/order/{xml}")

    order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    xml_skip = '''<operations>
            </operations>'''

    await rtc.send("/data/unit_table")

    units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')

    aircraft_number = 6
    while True:
        time.sleep(0.25)
        check = 0
        trigger = 0
        await rtc.send(f"/order/{xml_skip}")

        order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        order_result

        await rtc.send("/data/target_list")

        targets = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
        targets
        try:
            Target_dict = json.loads(targets[0]['data'])
            Target_dict
        except:
            break
        Target_list_temp=[]
        random_target = []
        for i in range(1,10):
            random_target_temp = 'T'+f'{i}'
            if(Target_dict['Targets'][random_target_temp]['threat'] == 0):
                check = check + 1

            if(Target_dict['Targets'][random_target_temp]['probability'] != 0 and Target_dict['Targets'][random_target_temp]['targeted'] != True):
                aircraft_number = aircraft_number + 1
                if (aircraft_number >= 30):
                    aircraft_number = aircraft_number % 30
                trigger = 1
                Target_list_temp.append(Target_dict['Targets'][random_target_temp])
                random_target.append(random_target_temp)
        if(check == 9):
            break
        if trigger == 1:
            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

            xml = \
f'''<operations>
    <order>
        <time>{"0"+str(int(units[0]['time'])+1)}</time>
        <base>{unit_dict[select_aircraft(Target_list_temp,1)[0][aircraft_number][0]]['Base']}</base>
        <aircraft_type>{aircraft_info[select_aircraft(Target_list_temp,1)[0][aircraft_number][0][0:2]]['Aircraft Type']}</aircraft_type>
        <track_number>{select_aircraft(Target_list_temp,1)[0][aircraft_number][0]}</track_number>
        <mission_type>1</mission_type>
        <course>{random_target[0]}</course>
    </order>
</operations>'''

            time.sleep(0.25)
            await rtc.send(f"/order/{xml}")

            order_result = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            order_result

            await rtc.send("/data/unit_table")

            units = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
            units

    await rtc.send("/result")

    msg = pd.DataFrame.from_dict(data=json.loads(await rtc.recv()), orient='index')
    print(msg)

main()
