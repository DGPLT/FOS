import asyncio
import websockets
import json

import pandas as pd

HOST = "127.0.0.1"
PORT = 8080


async def accept(websocket):
    async def recv():
        return (await websocket.recv()).decode()
    send = websocket.send

    # client accept
    print("receiving client")
    msg = await recv()
    print(msg)

    # start
    print("/start")
    await send("/start".encode())
    msg = pd.DataFrame.from_dict(data=json.loads(await recv()), orient='index')
    print(msg)
    input("press enter to continue...")

    # data get
    print("/data/aircraft_specsheet")
    await send("/data/aircraft_specsheet".encode())
    spec = pd.DataFrame.from_dict(data=json.loads(await recv()), orient='index')
    print(spec)
    input("press enter to continue...")
    print(pd.DataFrame.from_dict(data=json.loads(spec[0]['data']), orient='index'))
    input("press enter to continue...")

    print("/data/target_list")
    await send("/data/target_list".encode())
    targets = pd.DataFrame.from_dict(data=json.loads(await recv()), orient='index')
    print(targets)
    input("press enter to continue...")
    print(pd.DataFrame.from_dict(data=json.loads(targets[0]['data']), orient='columns'))
    input("press enter to continue...")

    print("/data/unit_table")
    await send("/data/unit_table".encode())
    units = pd.DataFrame.from_dict(data=json.loads(await recv()), orient='index')
    print(units)
    input("press enter to continue...")
    print(pd.DataFrame.from_dict(data=json.loads(units[0]['data']), orient='index'))
    input("press enter to continue...")

    xml = """<operations>
    <order>
        <time>0601</time>
        <base>A</base>
        <aircraft_type>Airplane</aircraft_type>
        <track_number>A4-B</track_number>
        <mission_type>1</mission_type>
        <course>T8</course>
    </order>
    <order>
        <time>0602</time>
        <base>B</base>
        <aircraft_type>Drone</aircraft_type>
        <track_number>D1-A</track_number>
        <mission_type>1</mission_type>
        <course>T8</course>
    </order>
</operations>"""

    print("/order")
    await send(f"/order/{xml}".encode())
    order_result = pd.DataFrame.from_dict(data=json.loads(await recv()), orient='index')
    print(order_result)
    input("press enter to continue...")


async def main():
    async with websockets.serve(accept, HOST, PORT):
        print(f"starting server on ws://{HOST}:{PORT}")
        await asyncio.Future()  # run forever

asyncio.run(main())
