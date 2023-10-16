from __future__ import annotations
from typing import Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message
    from abdes1.core import ActorSystem


class ActorProtocol(Protocol):
    id: str

    @property
    def actor_system(self) -> Optional[ActorSystem]:
        ...

    async def run(self) -> None:
        ...

    async def send_message(self, message: Message) -> None:
        ...
