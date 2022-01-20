from typing import Any, AsyncGenerator, Optional, Union
from requests.models import Response
from aiohttp import ClientSession as Session
from pathlib import Path
from abc import ABC, abstractmethod
from . import sslcontext
import aiofiles
import json

class GettableData(ABC):
    @abstractmethod
    async def get_data(self) -> Any:
        ...

class GettableWebData(GettableData):
    url: str
    name: str
    _json: bool
    _path: Optional[dict]
    __session: Session


    def __init__(self, url: str, name: str, session: Session, json: bool = True, path: str = None, **kwargs):
        self.url = url
        self.name = name
        self._json = json
        self._path = path
        self.__session = session

    def __repr__(self) -> str:
        return f"<name={self.name}, json={self._json}, path={self._path}>"

    async def __get_from_json(self, r: Response) -> Union[int, str]:
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

    async def __get_from_raw(self, r: Response) -> Union[int, str]:
        try:
            text = await r.text()
            return int(text)
        except ValueError:
            return text

    async def get_data(self) -> Union[int, str]:
        async with self.__session.get(self.url, ssl=sslcontext) as r:
            if r.status == 200:
                if self._json:
                    return await self.__get_from_json(r)
                else:
                    return await self.__get_from_raw(r)

class GettableDiskData(GettableData):
    name: str
    path: Path
    generator: AsyncGenerator

    def __init__(self, path: Path, name: str):
        self.name = name
        self.path = path
        self.generator = self.__line_generator()

    def __repr__(self) -> str:
        return f"<name={self.name}, path={self.path}>"

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