import os
import aiofiles
from aioconsole import ainput
from colorama import Fore as color


class Menu:
    def __str__(self):
        return f"""{color.LIGHTYELLOW_EX}
{color.LIGHTYELLOW_EX}██████╗░██╗░░░██╗██████╗░██╗███████╗██╗░░░██╗
{color.LIGHTYELLOW_EX}██╔══██╗██║░░░██║██╔══██╗██║██╔════╝╚██╗░██╔╝
{color.LIGHTYELLOW_EX}██████╔╝██║░░░██║██████╔╝██║█████╗░░░╚████╔╝░
{color.LIGHTYELLOW_EX}██╔═══╝░██║░░░██║██╔══██╗██║██╔══╝░░░░╚██╔╝░░
{color.LIGHTYELLOW_EX}██║░░░░░╚██████╔╝██║░░██║██║██║░░░░░░░░██║░░░            {color.RED}Github: https://github.com/Shell1010/Tox
{color.LIGHTYELLOW_EX}╚═╝░░░░░░╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░            {color.RED}Author: Shell
{color.LIGHTYELLOW_EX}============================================================================================={color.RESET}
        """

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    async def input(msg: str):
        return await ainput(
            f"""
{color.GREEN}╔═════════╣ PURIFY ╠ {msg}
{color.GREEN}║
{color.GREEN}╚═════[{color.LIGHTBLUE_EX}>{color.GREEN}]{color.RESET} """
        )

    @staticmethod
    async def write_file(resp: list[dict[str, str]]):
        for msg in resp:
            async with aiofiles.open(f"{msg.channel_id}.txt", "a+") as f:
                content = f"""
MESSAGE ID : {msg.id}
MESSAGE LINK: https://discord.com/channels/@me/{msg.channel_id}/{msg.id}
MESSAGE AUTHOR : {msg.author['username']}{msg.author['discriminator']}
{msg.content}\n"""
                if msg.guild_id is not None:
                    content = f"""
MESSAGE ID : {msg.id}
MESSAGE LINK: https://discord.com/channels/{msg.guild_id}/{msg.channel_id}/{msg.id}
MESSAGE AUTHOR : {msg.author['username']}{msg.author['discriminator']}
{msg.content}\n"""

                await f.write(f"{content}")
