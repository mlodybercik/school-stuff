from . import logger
logger = logger.getChild("aggregator_logic")

from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from typing import Collection, Dict, Any, List, Tuple

class AggregatorLogic(ABC):
    """base class for containing aggregator logic"""
    name: str

    @classmethod
    def status(cls) -> Dict[str, str]:
        return {"name": cls.name}

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]: ... # type: ignore

    @staticmethod
    def dataIsValid(data: Any) -> bool: ...

    @staticmethod
    def convertData(data: Any): ...

class ASum(AggregatorLogic):
    name = "sum"

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        logger.debug("Executing ASum")
        if not len(data):
            return {"value": 0,
                    "endpoints": {}}
        endpoints: Dict[str, float] = {}
        for endpoint, number in data:
            if endpoint in endpoints:
                endpoints[endpoint] += number
            else:
                endpoints[endpoint] = number
        sum_ = sum(endpoints.values())

        return {"value": sum_,
                "endpoints": endpoints}

    @staticmethod
    def dataIsValid(data: Any) -> bool:
        return isinstance(data, (int, float))

    @staticmethod
    def convertData(data: Any):
        return float(data)

class AMean(AggregatorLogic):
    name = "mean"

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        logger.debug("Executing AMean")
        if not len(data):
            return {"value": 0,
                    "endpoints": {}}
        endpoints: Dict[str, list] = {}
        #! i know, such a mess... ¯\_(ツ)_/¯
        for endpoint, number in data:
            if endpoint in endpoints:
                endpoints[endpoint][0] += 1
                endpoints[endpoint][1][0] += number
            else:
                endpoints[endpoint] = [1, [number]]
        
        endpoint_means = {k: v[1][0]/v[0] for k, v in endpoints.items()}
        mean = sum([v[1][0] for v in endpoints.values()])/len(data)

        
        return {"value": mean,
                "endpoints": endpoint_means}

    @staticmethod
    def dataIsValid(data: Any) -> bool:
        return isinstance(data, (int, float))

    @staticmethod
    def convertData(data: Any):
        return float(data)

class AMax(AggregatorLogic):
    name = "max"

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        logger.debug("Executing AMax")
        if not len(data):
            return {"value": 0,
                    "endpoints": {}}
        endpoints: Dict[str, float] = {}
        for endpoint, number in data:
            if endpoint in endpoints:
                if number > endpoints[endpoint]:
                    endpoints[endpoint] = number
            else:
                endpoints[endpoint] = number

        max_ = max(endpoints.values())
        
        return {"value": max_,
                "endpoints": endpoints}

    @staticmethod
    def convertData(data: Any):
        return float(data)

    @staticmethod
    def dataIsValid(data: Any) -> bool:
        return isinstance(data, (int, float))

class AMin(AggregatorLogic):
    name = "min"

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        logger.debug("Executing AMin")
        if not len(data):
            return {"value": 0,
                    "endpoints": {}}
        endpoints: Dict[str, float] = {}
        for endpoint, number in data:
            if endpoint in endpoints:
                if number < endpoints[endpoint]:
                    endpoints[endpoint] = number
            else:
                endpoints[endpoint] = number

        min_ = min(endpoints.values())
        
        return {"value": min_,
                "endpoints": endpoints}

    @staticmethod
    def dataIsValid(data: Any) -> bool:
        return isinstance(data, (int, float))

    @staticmethod
    def convertData(data: Any):
        return float(data)

class AAppend(AggregatorLogic):
    name = "append"

    @staticmethod
    def execute(data: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        logger.debug("Executing AAppend")
        if not len(data):
            return {"value": 0,
                    "endpoints": {}}
        endpoints: Dict[str, List[Any]] = {}
        for endpoint, value in data:
            if endpoint in endpoints:
                endpoints[endpoint].append(value)
            else:
                endpoints[endpoint] = [value]

        return {"endpoints": endpoints}

    @staticmethod
    def convertData(data: Any):
        return data

    @staticmethod
    def dataIsValid(data: Any) -> bool:
        return True