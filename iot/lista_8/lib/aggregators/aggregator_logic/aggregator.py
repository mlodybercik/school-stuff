import time
import itertools
from typing import Deque, Dict, Any, Tuple, Type, List
from collections import deque

from .aggregator_logic import AggregatorLogic
from ..graph_logic import GraphingLogic

MAX_RAW_AGGREGATED_LENGTH = 10_000

from . import logger
logger = logger.getChild("aggregator")

class Aggregator:
    """class for containing aggregated data without aggregator logic"""
    topic: str
    #* topic of the aggregator

    data: Tuple[Deque[float], Deque[Tuple[str, Any]]]
    #* data contains gathered data, with corresponding endpoint it has been posted to

    logic: Type["AggregatorLogic"]
    #* aggregator logic

    def __init__(self, topic: str, logic: Type["AggregatorLogic"], timeperiod: int, graph: GraphingLogic) -> None:
        assert isinstance(timeperiod, int) and timeperiod > 0

        self.topic = topic
        self.data = (deque(maxlen=MAX_RAW_AGGREGATED_LENGTH), # timestamps
                     deque(maxlen=MAX_RAW_AGGREGATED_LENGTH)) # actual data
        self.logic = logic
        self.timeperiod = timeperiod
        self.graph = graph

        logger.info(f"Creating new aggregator {logic.name} for /{topic}/... ")

    def receiveData(self, data, endpoint) -> bool:
        try:
            data = self.logic.convertData(data)
        except AttributeError:
            logger.warning(f"Couldn't convert data! /{self.topic}/{endpoint}, {data}")
            return False
        self.data[1].appendleft((endpoint, data))
        self.data[0].appendleft(time.time())
        logger.info(f"Receiving data from /{self.topic}/{endpoint}")
        return True

    def status(self) -> Dict[str, Any]:
        return {"warmed_up": self.data[0].maxlen == len(self.data[0]),
                "type": self.logic.name,
                "graph": self.graph.status(),
                "timeperiod": self.timeperiod}

    def getData(self) -> Dict[str, Any]:
        return self.logic.execute(self.prepareData()) # type: ignore

    def prepareData(self) -> List[Tuple[str, Any]]:
        from_ = time.time() - self.timeperiod
        i = 0
        for i, to in enumerate(self.data[0]):
            if from_ > to:
                break
        return list(itertools.islice(self.data[1], 0, i))[::-1] # type: ignore

    def getGraph(self, **kwargs):
        return self.graph.draw(self.prepareData(), **self.graph.parse_settings(kwargs))

    def changeAggregator(self, new: Type["AggregatorLogic"]) -> None:
        logger.info(f"Changing aggregator from {self.logic.name} to {new.name} on {self.topic}")
        if issubclass(new, AggregatorLogic):
            self.logic = new
            try:
                for i, item in enumerate(self.data[1]):
                    self.data[1][i] = (item[0], new.convertData(item[1]))
            except Exception as e:
                self.data = (deque(maxlen=MAX_RAW_AGGREGATED_LENGTH), # timestamps
                             deque(maxlen=MAX_RAW_AGGREGATED_LENGTH)) # actual data
                logger.error("Couldn't convert data to new type, rebuilding memory...")
                logger.exception(e)
        else:
            raise AttributeError("you can't change type to other than AggregatorLogic!")