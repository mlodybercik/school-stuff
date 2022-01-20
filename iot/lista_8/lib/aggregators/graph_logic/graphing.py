from abc import ABC
from typing import Dict, Collection, Optional, Tuple, Any
import io
import matplotlib.pyplot as plt

from .. import logger

params = {"ytick.color" : "black",
          "xtick.color" : "black",
          "axes.labelcolor" : "black",
          "axes.edgecolor" : "black",
          "figure.autolayout": True,
          "savefig.pad_inches": 0}
plt.rcParams.update(params)

class GraphingLogic(ABC):
    """base class for graphing logic"""
    name: str
    allowed_settings: Dict[str, Any] = {
        "size": (5, 6),
        "transparent": True,
        "dpi": 96,
    }

    @staticmethod
    def parse_settings(settings: Dict[str, str]) -> Dict[str, Any]:
        ret = {}
        if "x" in settings and "y" in settings:
            try:
                ret["size"] = (int(settings.pop("x")), int(settings.pop("y")))
            except ValueError:
                pass
        if "dpi" in settings:
            try:
                ret["dpi"] = int(settings.pop("dpi"))
            except ValueError:
                pass
        _ = __class__.allowed_settings.copy()
        
        _.update(ret)
        logger.info(f"Creating graph with settings {_}")
        return _
    

    @classmethod
    def status(cls) -> Dict[str, str]:
        return {"name": cls.name}

    @staticmethod
    def draw(data: Collection[Tuple[str, Any]],
             **kwargs) -> io.BytesIO: ... # type: ignore

class PlainPlot(GraphingLogic):
    name = "plainplot"

    @staticmethod
    def draw(data: Collection[Tuple[str, Any]],
             size: Tuple[float, float] = None,
             **kwargs) -> io.BytesIO:
        image = io.BytesIO()
        plt.figure(tight_layout = True, figsize=size, dpi=kwargs["dpi"])
        plt.plot([number for _, number in data], color="#007bff")
        plt.grid(True)
        plt.savefig(image, format="svg", transparent=kwargs["transparent"])

        return image

class HistogramPlot(GraphingLogic):
    name = "histogramplot"

    @staticmethod
    def draw(data: Collection[Tuple[str, Any]],
             size: Tuple[float, float] = None,
             **kwargs) -> io.BytesIO:
        image = io.BytesIO()
        plt.figure(tight_layout = True, figsize=size, dpi=kwargs["dpi"])
        plt.hist([number for _, number in data], color="#007bff")
        plt.grid(True)
        plt.savefig(image, format="svg", transparent=kwargs["transparent"])

        return image


        