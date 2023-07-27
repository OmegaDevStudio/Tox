import os

from aioconsole import ainput
from colorama import Fore as color
from pystyle import Colorate, Colors


class Menu:

    def __str__(self):
        return f"""{color.LIGHTYELLOW_EX}
{color.LIGHTYELLOW_EX}██████╗░██╗░░░██╗██████╗░██╗███████╗██╗░░░██╗
{color.LIGHTYELLOW_EX}██╔══██╗██║░░░██║██╔══██╗██║██╔════╝╚██╗░██╔╝
{color.LIGHTYELLOW_EX}██████╔╝██║░░░██║██████╔╝██║█████╗░░░╚████╔╝░
{color.LIGHTYELLOW_EX}██╔═══╝░██║░░░██║██╔══██╗██║██╔══╝░░░░╚██╔╝░░
{color.LIGHTYELLOW_EX}██║░░░░░╚██████╔╝██║░░██║██║██║░░░░░░░░██║░░░            {color.RED}Github: https://github.com/Shell1010
{color.LIGHTYELLOW_EX}╚═╝░░░░░░╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░            {color.RED}Author: Shell
{color.LIGHTYELLOW_EX}============================================================================================={color.RESET}
        """

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    async def input(msg:str):
        return await ainput(f"""
{color.GREEN}╔═════════╣ PURIFY ╠ {msg}
{color.GREEN}║
{color.GREEN}╚═════[{color.LIGHTBLUE_EX}>{color.GREEN}]{color.RESET} """)
