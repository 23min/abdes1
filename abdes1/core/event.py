from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Actor, Message


@dataclass
class Event:
    time: float
    target_actor: Actor
    message: Message
