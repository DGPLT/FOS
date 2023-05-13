import asyncio

HOST = "127.0.0.1"
PORT = 8080
SIZE = 1024

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while data != "quit":
        data = (await reader.read(SIZE)).decode('utf8')
        addr, port = writer.get_extra_info("peername")

        message = data + '\n'
        writer.write(message.encode('utf8'))

        await writer.drain()
    writer.close()
    await writer.wait_closed()

async def run_server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())

#loop = asyncio.new_event_loop()
#loop.run_until_complete(run_server())
