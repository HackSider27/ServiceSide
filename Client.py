import asyncio
import os

import aiohttp
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/') as resp:
            print(resp.status)
            print(await resp.text())
        async with session.ws_connect('http://localhost:8080/ws') as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        if msg.data == 'Login: ':
                            print(msg.data)
                            str=input()
                            await ws.send_str(str)
                        elif msg.data == 'Password: ':
                            print(msg.data)
                            str = input()
                            await ws.send_str(str)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
loop = asyncio.get_event_loop()
loop.run_until_complete(main())