from typing import Any, AsyncGenerator, Literal, Union
from aiohttp import ClientSession as Session, ClientResponse
from pathlib import Path
from abc import ABC, abstractmethod
from . import sslcontext
import aiofiles
import json

class Getter(ABC):
    @abstractmethod
    async def get_data(self) -> Any: ...

    @abstractmethod
    def status(self) -> dict[str, Any]: ...

class GettableWebData(Getter):
    url: str
    _json: bool
    _path: str
    __session: Session

    def __init__(self, url: str, path: str, json: bool = True, session: Session = None):
        self.url = url
        self._json = json
        self._path = path
        if not session:
            self.__session = Session()
        else:
            self.__session = session

    def __repr__(self) -> str:
        return f"<son={self._json}, path={self._path}>"

    async def __get_from_json(self, r: ClientResponse) -> Union[int, str, Literal[None]]:
        try:
            data = await r.json()
        except json.decoder.JSONDecodeError:
            return None

        for item in self._path.split(" "):
            if isinstance(data, dict):
                data = data[item]
            else:
                data = data[int(item)]

        try:
            return int(data)
        except ValueError:
            return data

    async def __get_from_raw(self, r: ClientResponse) -> Union[int, str, Literal[None]]:
        try:
            text = await r.text()
            return int(text)
        except ValueError:
            return text

    async def get_data(self) -> Union[int, str, Literal[None]]:
        async with self.__session.get(self.url, ssl=sslcontext) as r:
            if r.status == 200:
                if self._json:
                    return await self.__get_from_json(r)
                else:
                    return await self.__get_from_raw(r)
            return None

    def status(self):
        return {"type":"webdata", "url": self.url, "json": self._json, "path": self._path}

class GettableDiskData(Getter):
    path: Path
    generator: AsyncGenerator

    def __init__(self, path: Path):
        self.path = path
        self.generator = self.__line_generator()

    def __repr__(self) -> str:
        return f"<path={self.path}>"

    async def __line_generator(self):
        async with aiofiles.open(self.path, "r") as file:
            async for line in file:
                yield line

    async def get_data(self) -> str:
        try:
            return await self.generator.__anext__()
        except StopAsyncIteration as e:
            self.generator = self.__line_generator()
            return await self.generator.__anext__()

    def status(self):
        return {"type":"diskdata", "path": self.path}