import asyncio
import os
import json
from aioconsole import aprint
from colorama import Fore as color

from src import Menu, Tox, Handler


with open("./config.json", "r") as f:
    config = json.load(f)


if config["token"] != "":
    TOKEN = config["token"]
else:
    TOKEN = input(f"{color.GREEN}Please input your token.{color.RESET}")
tox = Handler()


async def main():
    if not await Tox.validate(TOKEN):
        raise RuntimeError("Invalid Token. YOU SUCKETH BALLS.")
    menu = Menu()
    menu.clear()
    await aprint(menu)
    await tox.show_cmds()
    while True:
        inp = await menu.input("Please enter your option.")
        cmd = tox.handle_input(inp)
        if cmd is not None:
            await aprint()
            await cmd.func()


@tox.cmd(description="Shows command help")
async def help():
    await tox.show_cmds()

@tox.cmd(description="Clears the terminal")
async def clear():
    menu = Menu()
    menu.clear()
    await aprint(menu)


@tox.cmd(description="Reports a guild using an id")
async def guild_report():
    menu = Menu()
    menu.clear()
    await aprint(menu)

    reporter = Tox(0)
    guild_id = config["guild_id"]
    if guild_id == "":
        await reporter.load("guild")
    else:
        await reporter.load("guild", guild_id=guild_id)
    await reporter.show_options()
    amount = int(
        await menu.input("Please input how many times you'd like to send the report")
    )
    await aprint(await reporter.trigger(TOKEN, amount))


@tox.cmd(description="Reports a message using a link")
async def msg_report():
    menu = Menu()
    menu.clear()
    await aprint(menu)

    reporter = Tox(3)
    link = config["link"]
    if link == "":
        await reporter.load("message")
    else:
        await reporter.load("message", link=link)
    await reporter.show_options()
    amount = int(
        await menu.input("Please input how many times you'd like to send the report")
    )
    await aprint(await reporter.trigger(TOKEN, amount))


@tox.cmd(description="Filters message content within a guild")
async def scrape_guild():
    menu = Menu()
    reporter = Tox()
    guild_id = config["guild_id"]
    if guild_id == "":
        await reporter.load("guild")
    else:
        await reporter.load("guild", guild_id=guild_id)
    content = await menu.input("Please input the message content you wish to search for.")
    msgs = await reporter.filter_guild(TOKEN, content)
    await menu.write_file(msgs)

@tox.cmd(description="Filters message content within a channel")
async def scrape_channel():
    menu = Menu()
    reporter = Tox()
    channel_id = config['channel_id']
    if channel_id == "":
        channel_id = await menu.input("Please input the channel_id you would like to search.")
    content = await menu.input("Please input message content you wish to search for.")
    msgs = await reporter.filter_channel(TOKEN, channel_id, content)
    await menu.write_file(msgs)
asyncio.run(main())
