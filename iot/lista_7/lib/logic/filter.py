from typing import Dict, List, TypeVar, Any
import shlex

from . import logger

JSON = Dict[str, Any]

class Filter:
    def __init__(self, paths: List[str], soft = True):
        self.paths = paths
        self.soft = soft

    def filter(self, data: JSON):
        out = {}
        for path in self.paths:
            curr = data
            try:
                for key in shlex.split(path):
                    if key != "*":
                        curr = curr[key]
                    else:
                        break
            except KeyError:
                logger.warning(f"while executing '{path}' encoutnered KeyError, missing {key}")
                if not self.soft:
                    return None
            if key != "*":
                out[key] = curr
            else: 
                out.update(curr)
        return out

    def status(self):
        return {"soft": self.soft,
                "paths": self.paths}