from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    content: Any
    time: float  # Simulation time when the message should be processed
