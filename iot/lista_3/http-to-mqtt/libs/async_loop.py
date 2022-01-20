import asyncio
import json
from datetime import datetime

from .get_data import GettableWebData
from .post_data import Poster

class AsyncLoop:
    source: GettableWebData
    sink: Poster
    sleep: int
    end: bool

    def __init__(self, data_source: GettableWebData, data_sink: Poster, sleep: int):
        self.source = data_source
        self.sink = data_sink
        self.sleep = sleep
        self.end = False

    async def loop(self):
        while not self.end:
            try:
                data = str(await self.source.get_data())
                sendable = json.dumps(
                    {"t": str(datetime.utcnow()),
                    self.source.name: data}
                )
                await self.sink.post(self.source.name, sendable)
                await asyncio.sleep(self.sleep)

            except asyncio.CancelledError:
                self.end = True
            
            except Exception as e:
                self.end = True
                raise e