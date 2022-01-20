import asyncio
from .network.sender import Sender
from .network.getter import Getter

from .logic.filter import Filter

from . import logger

logger = logger.getChild("manager")

class Loop:
    running: bool
    getter: Getter
    sender: Sender
    period: int
    shouldStop: bool
    filter: Filter
    __future: asyncio.Future
    loops: int
    successful_loops: int

    def __init__(self, name: str, getter: Getter, sender: Sender, period: int, filter: Filter):
        self.name = name
        self.filter = filter
        self.getter = getter
        self.sender = sender
        self.period = period
        self.shouldStop = False
        self.running = False
        self.loops = 0
        self.successful_loops = 0

    async def start(self):
        self.running = True
        self.__future = asyncio.ensure_future(self.loop())
        return self.__future

    async def loop(self):
        async with self.sender as send:
            while not self.shouldStop:
                try:
                    data = await self.getter.get_data()
                    if (data := self.filter.filter(data)):
                        self.successful_loops += 1
                        await send.send({"data": data})
                    
                    self.loops += 1
                    await asyncio.sleep(self.period)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.exception(e)
        self.shouldStop = False
        self.running = False

    async def exit(self):
        self.shouldStop = True
        try:
            self.__future.cancel()
        except asyncio.CancelledError:
            pass
        while not self.__future.done():
            await asyncio.sleep(0.05)
        return True

    def status(self):
        return {"name": self.name,
                "type": "generator-filter",
                "running": self.running,
                "period": self.period, 
                "sender": self.sender.status(),
                "filter": self.filter.status(),
                "getter": self.getter.status(),
                "iterations": self.loops,
                "successful_iterations": self.successful_loops}

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
