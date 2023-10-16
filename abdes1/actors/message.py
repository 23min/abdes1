from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    content: Any
    from_id: str  # todo address
    to_id: str  # todo address
    time: float  # Simulation time when the message should be processed
