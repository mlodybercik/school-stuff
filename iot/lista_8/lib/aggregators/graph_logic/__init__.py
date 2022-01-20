from typing import Mapping
from .. import logger
logger = logger.getChild("graph")
from .graphing import GraphingLogic, PlainPlot, HistogramPlot

graph_enum: Mapping[str, GraphingLogic] = {
    "plain": PlainPlot,
    "histogram": HistogramPlot
}
