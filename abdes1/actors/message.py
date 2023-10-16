from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    content: Any
    from_id: str  # todo this should be an address
    to_id: str  # todo this should be an address
    time: float  # Simulation time when the message should be processed
    # TODO: Perhaps have "scheduled_time" and "processed_time" fields
