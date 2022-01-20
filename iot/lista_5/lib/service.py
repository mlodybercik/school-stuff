import aiohttp
import asyncio
from typing import Literal, Union, Dict, Any, List
from dataclasses import dataclass
from inspect import currentframe, getframeinfo

from . import sslcontext, logger

logger = logger.getChild("service")

import aiohttp

class Service:
    name: str
    address: str
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self) -> str:
        return f"<Service name={self.name} address={self.address}>"

    async def get_status(self, status = "/api/status") -> Union[Literal[False], Dict[str, Any]]:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(1)) as session:
            try:
                async with session.get(self.address + status, ssl=sslcontext) as r:
                    if r.status != 200:
                        logger.warning("statuscode for endpoint != 200")
                        return False
                    if not (data := await r.json()):
                        logger.warning("endpoint didn't return JSON data")
                        return False

                    return data
            except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
                logger.critical(f"Couldn't connect to endpoint! is {self.address} even alive?")
                return False

    async def update(self, path: str, data: dict[str, Any]) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                address = self.address + f"/api/{path}"
                async with session.post(address, json=data, ssl=sslcontext) as r:
                    if r.status != 200:
                        logger.warning(f"status for endpoint != 200, {await r.json()}")
                        return False
                    else:
                        return True

            except aiohttp.ClientConnectionError as e:
                logger.critical(f"Couldn't connect to endpoint! is {address} even alive?")

            except aiohttp.ContentTypeError as e:
                logger.error(f"Other side prolly did an oopsie owo {address}")
                logger.exception(e)

        return False

    async def get(self, path: str, data: dict[str, Any]) -> Any:
        async with aiohttp.ClientSession() as session:
            try:
                address = self.address + path
                async with session.get(address, json=data, ssl=sslcontext) as r:
                    if r.status != 200:
                        logger.warning(f"get failed, status for endpoint != 200, {address}")
                        return None
                    else:
                        return await r.read()

            except aiohttp.ClientConnectionError as e:
                logger.critical(f"Couldn't connect to endpoint! is {address} even alive?")

            except aiohttp.ContentTypeError as e:
                logger.error(f"Other side prolly did an oopsie owo {address}")
                logger.exception(e)   


@dataclass(repr=False)
class Manager:
    services: Dict[str, Service]

    def __init__(self) -> None:
        self.services = {}

    def __iter__(self):
        return self.services.__iter__()

    def __getitem__(self, key):
        return self.services[key]

    def __repr__(self):
        return self.service.__repr__()

    def __setitem__(self, key, item):
        self.services[key] = item

class Generator:
    @staticmethod
    async def handle_change_sender(service: Service, form: Dict[str, Any]):
        if "address" in form and "topic" in form:
            return await service.update("change_sender", form)

        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_change_getter(service: Service, form: Dict[str, Any]):
        if "type" in form and "url" in form and "json" in form and "path" in form:
            return await service.update("change_getter", form)

        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_toggle_pause(service: Service, form: Dict[str, Any]):
        return await service.update("toggle_pause", form)

class Aggregator:
    @staticmethod
    async def handle_add_aggregator(service: Service, form: Dict[str, Any]):
        if "type" in form and "time" in form and "name" in form:
            return await service.update("register/", form)

        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_change_aggregator(service: Service, form: Dict[str, Any]):
        if "type" in form and "time" in form and "name" in form:
            return await service.update("change/", form)

        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_remove_aggregator(service: Service, form: Dict[str, Any]):
        if "name" in form:
            return await service.update("remove/", form)

        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

class FilterGenerator:

    @staticmethod
    async def handle_toggle_pause(service: Service, form: Dict[str, Any]):
        return await service.update("toggle_pause", form)

    @staticmethod
    async def handle_change_getter(service: Service, form: Dict[str, Any]):
        if "url" in form:
            return await service.update("change_getter", form)
        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_change_sender(service: Service, form: Dict[str, Any]):
        if "address" in form and "topic" in form:
            return await service.update("change_sender", form)
        logger.warning(f"missing keys inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

    @staticmethod
    async def handle_change_filter(service: Service, form: Dict[str, Any]):
        if "soft" in form and "paths" in form and isinstance(form["paths"], list):
            return await service.update("change_filter", form)
        logger.warning(f"missing keys or type mismatch inside {getframeinfo(currentframe()).function}") # type: ignore
        return False

class GraphingAggregator:

    @staticmethod
    async def handle_change(service, form: Dict[str, Any]):
        if "agg_type" in form and "graph_type" in form and "time" in form:
            return await service.update("change/", form)
    logger.warning(f"missing keys or type mismatch inside {getframeinfo(currentframe()).function}") # type: ignore
