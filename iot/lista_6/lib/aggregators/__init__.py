from typing import Mapping
from .. import logger

from .aggregator_logic import AAppend, AMax, AMin, AMean, ASum, AggregatorLogic
from .aggregator import Aggregator

enum: Mapping[str, AggregatorLogic] =  {
    "append": AAppend,
    "max": AMax,
    "min": AMin,
    "mean": AMean,
    "sum": ASum,
}