from typing import Union, Any
from amqtt.client import MQTTClient
from aiohttp import ClientSession as Session
from abc import ABC, abstractmethod
from . import logger

logger = logger.getChild("sender")

class Sender(ABC):
    @abstractmethod
    async def setup(self) -> None: ...
    @abstractmethod
    async def send(self, data: Union[str, bytes]) -> None: ...
    @abstractmethod
    async def teardown(self) -> None: ...
    @abstractmethod
    def status(self) -> dict[str, Any]: ...

class SenderMQTT(Sender):
    _client: MQTTClient
    def __init__(self, address: str, topic: str):
        self.address = address
        self.topic = topic
        self._client = MQTTClient()

    async def setup(self):
        await self._client.connect(self.address)
        logger.info("Connected to MQTT broker")

    async def send(self, data):
        data = bytes(str(data), "utf-8")
        await self._client.publish(self.topic, data)
        logger.info(f"MQTT: Sent data to {self.topic}")

    async def teardown(self):
        await self._client.disconnect()
        logger.info("MQTTClient teardown")

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, *_):
        await self.teardown()

    def status(self):
        return {"type": "sendermqtt", "address": self.address, "topic": self.topic}

class SenderHTTP(Sender):
    _session: Session
    def __init__(self, address: str, topic: str):
        assert not address.endswith("/")
        assert topic.startswith("/")

        logger.info(f"Creating HTTP object <address={address} topic={topic}>")
        self.address = address
        self._session = Session()
        self.topic = topic

    async def setup(self):
        logger.info("Sender HTTP setup")

    async def send(self, data):
        async with self._session.post(url = self.address + self.topic, data=data) as r:
            if r.status != 200:
                logger.error("Status code != 200")
            else:
                logger.info(f"HTTP: Sent data to {self.topic}")

    async def teardown(self):
        logger.info("HTTP teardown")

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, *_):
        import sys, traceback
        for item in traceback.format_exception(*sys.exc_info()):
            logger.debug(item[:-1])
        await self.teardown()

    def status(self):
        return {"type": "sendermqtt", "address": self.address, "topic": self.topic}