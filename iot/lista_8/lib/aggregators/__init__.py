from typing import Mapping

from .. import logger

from .aggregator_logic.aggregator_logic import AAppend, AMax, AMin, AMean, ASum, AggregatorLogic
from .graph_logic.graphing import GraphingLogic
from .aggregator_logic.aggregator import Aggregator

aggregator_enum: Mapping[str, AggregatorLogic] = {
    #"append": AAppend,
    "max": AMax,
    "min": AMin,
    "mean": AMean,
    "sum": ASum,
}
