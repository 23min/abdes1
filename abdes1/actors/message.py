from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    content: Any
    from_id: str  # TODO this should be an address
    to_id: str  # TODO this should be an address
    time: float  # TODO Should we have sent_time and received_time?
    # TODO: Also, for DES, we need "scheduled_time" for the future event list
