from typing import Protocol
from amqtt.client import MQTTClient, ClientException
from aiohttp import ClientSession as Session
from . import sslcontext

class Poster(Protocol):
    async def setup(self, **kwg) -> bool:
        ...
    async def post(self, dest: str, data: str) -> bool:
        ...
    async def teardown(self, **kwg) -> bool:
        ...


class MQTTPoster(Poster):
    """
    Dedicated class for posting data to MQTT broker
    it uses established connection to post data.
    """
    client: MQTTClient
    prepend: str
    __connected: bool

    @staticmethod
    async def create_mqtt_from_dict(schema: str, port: int, url: int, **kwargs) -> MQTTClient:
        client = MQTTClient()
        await client.connect(f"{schema}://{url}:{port}")
        return client

    def __init__(self):
        self.__connected = False

    async def setup(self, client: MQTTClient, prepend: str) -> bool:
        self.prepend = prepend
        if self.__connected:
            return False
        self.client = client
        self.__connected = True
        return True

    async def post(self, dest: str, data: str) -> bool:
        if self.__connected:
            try:
                await self.client.publish(self.prepend + dest, bytes(data, encoding="utf-8"))
                return True
            except ClientException:
                pass
        return False

    async def teardown(self) -> bool:
        if self.__connected:
            await self.client.disconnect()
            self.__connected = False
            return True
        return False

class HTTPPoster(Poster):
    __connected: bool
    session: Session
    ssl = sslcontext
    prepend: str

    def __init__(self):
        self.session = None

    async def setup(self, session: Session, schema: str, port: int, url: str, path: str) -> bool:
        self.prepend = f"{schema}://{url}:{port}{path}"
        if session:
            self.session = session
            return True
        elif not self.session:
            self.session = Session()
            return True
        return False

    async def post(self, dest: str, data: str) -> bool:
        async with self.session.post(self.prepend + dest, data=data, ssl=sslcontext) as r:
            return r.status == 200

    async def teardown(self) -> bool:
        if self.session:
            await self.session.close()
            self.session = None
            return True
        return False
