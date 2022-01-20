from typing import Any, Literal, Union
from aiohttp import ClientSession as Session, ClientResponse
from abc import ABC, abstractmethod
from . import sslcontext
import json

class Getter(ABC):
    @abstractmethod
    async def get_data(self) -> Any: ...

    @abstractmethod
    def status(self) -> dict[str, Any]: ...

class GettableWebData(Getter):
    url: str
    _path: str
    __session: Session

    def __init__(self, url: str, session: Session = None):
        self.url = url
        if not session:
            self.__session = Session()
        else:
            self.__session = session

    def __repr__(self) -> str:
        return f"<Getter url={self.url}>"

    async def __get_from_json(self, r: ClientResponse) -> Union[int, str, Literal[None]]:
        try:
            return await r.json()
        except json.decoder.JSONDecodeError:
            return None

    async def get_data(self) -> Union[str, Literal[None]]:
        async with self.__session.get(self.url, ssl=sslcontext) as r:
            if r.status == 200:
                return await self.__get_from_json(r)
            return None

    def status(self):
        return {"type":"webdata", "url": self.url}