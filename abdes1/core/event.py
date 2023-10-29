from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
import functools

if TYPE_CHECKING:
    from abdes1.actors import Message


@functools.total_ordering
@dataclass
class Event:
    message: Message
    time: Optional[float] = None

    def __post_init__(self):
        if self.time is None:
            self.time = 0.0

    def __lt__(self, other: "Message") -> bool:
        if (self.time is None) or (other.time is None):
            return False
        return self.time < other.time
