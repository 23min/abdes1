"""
registry.py

Registers actors and provides a lookup service.
"""
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorProtocol
from abdes1.utils import logging


class Registry:
    def __init__(self) -> None:
        self.actors: List[ActorProtocol] = []
        logging.log_event("-registry-", "Registry created")

    def register_actor(self, actor: ActorProtocol) -> None:
        self.actors.append(actor)
        logging.log_event("-registry-", f"Actor '{actor.id}' registered")

    def find_actor(self, target_actor: str) -> Optional[ActorProtocol]:
        for actor in self.actors:
            if actor.id == target_actor:
                return actor
            else:
                continue
        logging.log_event("-registry-", f"Actor '{target_actor}' not found")
        return None
