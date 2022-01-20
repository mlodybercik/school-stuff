import pytest
from collections import deque
from .aggregator_logic import AAppend, AMax, AMin, AMean, ASum

# data: Deque[Tuple[str, Any]]

@pytest.fixture
def numeric_deque():
    _ = [("r1", 7), ("r2", 12), ("r3", -3), ("r1", 3), ("r2", 15)]
    return deque(_, maxlen=10)

@pytest.fixture
def other_deque():
    _ = [("r1", "siema eniu"), ("r1", "siema jeszcze raz"), ("r2", 123), ("r3", "2137")]
    return deque(_, maxlen=10)

def test_ASum(numeric_deque):
    test = ASum.execute(numeric_deque)

    assert test["value"] == 34
    assert test["endpoints"] == {"r1": 10, "r2": 27, "r3": -3}

def test_AMean(numeric_deque):
    test = AMean.execute(numeric_deque)
    
    assert test["value"] == 6.8
    assert test["endpoints"] == {"r1": 5.0, "r2": 13.5, "r3": -3.0}

def test_AMin(numeric_deque):
    test = AMin.execute(numeric_deque)

    assert test["value"] == -3
    assert test["endpoints"] == {"r1": 3, "r2": 12, "r3": -3}

def test_AMax(numeric_deque):
    test = AMax.execute(numeric_deque)

    assert test["value"] == 15
    assert test["endpoints"] == {"r1": 7, "r2": 15, "r3": -3}

def test_AAppend(other_deque):
    test = AAppend.execute(other_deque)

    assert test["endpoints"] == {"r1": ["siema eniu", "siema jeszcze raz"],
                                 "r2": [123],
                                 "r3": ["2137"]}