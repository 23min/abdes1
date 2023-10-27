from dataclasses import dataclass
from typing import Any, Optional
import functools


@functools.total_ordering
@dataclass
class Message:
    type: str
    content: Any
    # TODO this should be an address
    from_id: str
    # TODO this should be an address
    to_id: str
    # TODO Should we have sent_time and received_time?
    time: Optional[float] = None
    scheduled_time: Optional[float] = None

    def __lt__(self, other: "Message") -> bool:
        if (self.scheduled_time is None) or (other.scheduled_time is None):
            return False
        return self.scheduled_time < other.scheduled_time
