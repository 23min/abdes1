from __future__ import annotations
from typing import Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message
    from abdes1.core import ActorSystem, Event


class EventLoopProtocol(Protocol):
    @property
    def actor_system(self) -> Optional[ActorSystem]:
        ...

    async def run(self) -> None:
        ...

    def dispatch_message(self, message: Message) -> None:
        ...

    def schedule_event(self, event: Event) -> None:
        ...

    # TODO: This does not belong here! This needs to be in a DES event loop
    def current_time(self) -> None:
        ...
