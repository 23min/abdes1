from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message
    from abdes1.core import ActorSystem, Event


class EventLoopProtocol(Protocol):
    actor_system: ActorSystem

    # @property
    # def actor_system(self) -> Optional[ActorSystem]:
    #     ...

    async def run(self) -> None:
        ...

    def dispatch_message(self, message: Message) -> None:
        ...

    def schedule_event(self, event: Event) -> None:
        ...
