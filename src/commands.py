from typing import Coroutine
import inspect
from aioconsole import aprint
from colorama import Fore as Color


class Command:
    def __init__(self, name: str, func: Coroutine, description: str):
        self.name = name
        self.func = func
        self.desc = description


class Handler:
    def __init__(self):
        self.commands: dict[str, Command] = {}

    def cmd(self, description: str):
        """Decorator for tools because I wanna make shit easier for me"""

        def decorator(coro: Coroutine):
            name = coro.__name__
            if name in self.commands:
                raise RuntimeError("This Command was already created YOU SUCK")
            if not inspect.iscoroutinefunction(coro):
                raise RuntimeError("Not a coroutine you SUCK BALLS!")

            cmd = Command(name, coro, description)
            self.commands[name] = cmd
            return cmd

        return decorator

    def handle_input(self, input: str) -> Coroutine:
        cmd = self.commands.get(input)
        return cmd

    async def show_cmds(self):
        for key, value in self.commands.items():
            await aprint(
                f"{Color.RED}[ {key} ]  :  {Color.GREEN}{value.desc}{Color.RESET}"
            )
