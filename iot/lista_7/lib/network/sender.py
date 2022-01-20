import json
from typing import Union, Any
from amqtt.client import MQTTClient
from aiohttp import ClientSession as Session, ClientTimeout, ContentTypeError
from asyncio import TimeoutError
from abc import ABC, abstractmethod
from . import logger

logger = logger.getChild("sender")

class Sender(ABC):
    @abstractmethod
    async def setup(self) -> None: ...
    @abstractmethod
    async def send(self, data: Union[str, bytes]) -> bool: ...
    @abstractmethod
    async def teardown(self) -> None: ...
    @abstractmethod
    def status(self) -> dict[str, Any]: ...

class SenderHTTP(Sender):
    TIMEOUT = 2
    _session: Session
    def __init__(self, address: str, topic: str):
        assert not address.endswith("/")
        assert topic.startswith("/")

        logger.info(f"Creating HTTP object <address={address} topic={topic}>")
        self.address = address
        self.topic = topic

    async def setup(self):
        self._session = Session(timeout=ClientTimeout(total=self.TIMEOUT))
        logger.info("Sender HTTP setup")

    async def teardown(self):
        await self._session.close()
        logger.info("HTTP teardown")

    async def send(self, data) -> bool:
        try:
            async with self._session.post(url = self.address + self.topic, json=data) as r:
                if r.status != 200:
                    logger.error(f"Status code != 200 {await r.json()}")
                else:
                    logger.info(f"HTTP: Sent data to {self.topic}")
                    return True
        except (TimeoutError, ContentTypeError):
            pass
        return False

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, *_):
        import sys, traceback
        for item in traceback.format_exception(*sys.exc_info()):
            logger.debug(item[:-1])
        await self.teardown()

    def status(self):
        return {"type": "senderhttp", "address": self.address, "topic": self.topic}