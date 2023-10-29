"""
registry.py

Registers actors and provides a lookup service.
"""
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorProtocol
from abdes1.utils.logger import ALogger


class Registry:
    def __init__(self) -> None:
        self.actors: List[ActorProtocol] = []
        self.logger = ALogger("-registry-")
        self.logger.info("Registry created")

    def register_actor(self, actor: ActorProtocol) -> None:
        self.actors.append(actor)
        self.logger.debug(f"Actor '{actor.id}' registered")

    def find_actor(self, target_actor: str) -> Optional[ActorProtocol]:
        for actor in self.actors:
            if actor.id == target_actor:
                return actor
            else:
                continue
        self.logger.debug(f"Actor '{target_actor}' not found")
        return None
