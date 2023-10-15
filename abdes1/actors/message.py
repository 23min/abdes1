from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    content: Any
    fromId: str  # todo address
    toId: str  # todo address
    time: float  # Simulation time when the message should be processed
