"""

registry.py

Registers actors and provides a lookup service.

"""
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorProtocol


class Registry:

    def __init__(self) -> None:
        self.actors: List[ActorProtocol] = []
        print("Registry created")

    def register_actor(self, actor: ActorProtocol) -> None:
        self.actors.append(actor)
        print(f"Actor {actor.id} registered")

    def find_actor(self, target_actor: str) -> Optional[ActorProtocol]:
        for actor in self.actors:
            if actor.id == target_actor:
                return actor
            else:
                continue
        print(f"Actor {target_actor} not found")
        return None
