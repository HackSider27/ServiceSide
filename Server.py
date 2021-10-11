import asyncio
import os
from aiohttp import WSMsgType
from aiohttp import web
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
PASSWORD = '20'

async def testhandle(request):
    return web.Response(text='Test handle')


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_str('Login: ')
    async for msg in ws:

        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            if msg.data != PASSWORD:
                await ws.send_str('Password: ')

        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


def main():
    #loop = asyncio.get_event_loop()
    app = web.Application()
    app.router.add_route('GET', '/', testhandle)
    app.add_routes([web.get('/ws', websocket_handler)])
    web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
