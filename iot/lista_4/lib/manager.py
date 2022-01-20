import asyncio
from typing import Dict
from .sender import Sender
from .getter import Getter

class Loop:
    running: bool
    getter: Getter
    sender: Sender
    period: int
    shouldStop: bool
    __future: asyncio.Future
    loops: int

    def __init__(self, name: str, getter: Getter, sender: Sender, period: int):
        self.name = name
        self.getter = getter
        self.sender = sender
        self.period = period
        self.shouldStop = False
        self.running = False
        self.loops = 0

    async def start(self):
        self.running = True
        self.__future = asyncio.ensure_future(self.loop())
        return self.__future

    async def loop(self):
        async with self.sender as send:
            while not self.shouldStop:
                try:
                    data = await self.getter.get_data()
                    await send.send(data)
                    self.loops += 1
                    await asyncio.sleep(self.period)
                except asyncio.CancelledError:
                    break
        self.shouldStop = False
        self.running = False

    async def exit(self):
        self.shouldStop = True
        try:
            self.__future.cancel()
        except asyncio.CancelledError:
            pass
        while not self.__future.done():
            await asyncio.sleep(0.1)
        return True

    def status(self):
        return {"name": self.name,
                "type": "generator",
                "running": self.running,
                "period": self.period, 
                "sender": self.sender.status(), 
                "getter": self.getter.status(),
                "iterations": self.loops}


class Manager:
    running: bool = False
    instance: Loop
    name: str

    def __init__(self, name=None):
        self.instance = None
        self.name = name

    def register_loop(self, loop: Loop):
            self.instance = loop
            
    async def run(self):
        if not self.running or self.name is not None:
            return asyncio.ensure_future(
                asyncio.gather(self.instance.start())
            )
        else:
            raise Exception("manager is running or no name is set")
    
    def set_name(self, name):
        self.name = name

    def status(self) -> dict[str, str]:
        return self.instance.status()
