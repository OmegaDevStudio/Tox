import asyncio
import os
from configparser import ConfigParser

from aioconsole import aprint
from colorama import Fore as color

from src import Menu, Tox

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

config = ConfigParser()
config.read("config.ini")

async def main():
    menu = Menu()
    menu.clear()
    token = config['USER']['Token']
    await aprint(menu)
    if token == "":
        token = await menu.input("Please input your token.")
    if await Tox.validate(token):
        opt = await menu.input("Please input the report type.")
        if opt.lower() == "message":
            tox = Tox(3)
            link = config['USER']['Link']
            if link == "":
                await tox.load("message")
            else:
                await tox.load("message", link=link)
            await tox.show_options()
            await tox.trigger(token)
        else:
            tox = Tox(0)
            guild = config['USER']['Guild']

            if guild == "":
                await tox.load("guild")
            else:
                await tox.load("guild", guild_id=guild)
            await tox.show_options()
            await tox.trigger(token)
    else:
        await aprint(f"{color.RED}Invalid Token: {token}{color.RESET}")
    
if __name__ == "__main__":
    asyncio.run(main())
