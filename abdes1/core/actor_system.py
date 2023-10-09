"""

actor_system.py

The core of the actor system which handles

- actor lifecycle (create, start, stop)
- actor registration and discovery
- propagation of events
- ...

The event loop is responsible for scheduling events and propagating them to the actors.
The event loop is also responsible for scheduling the actors to run concurrently.

The event loop is tightly integrated with a model of computation.
For example, in a discrete event simulation, time progresses as events occur.
It should be possible to use different models of computation, but for this
first iteration a DES compatible event loop will be used.

"""
from __future__ import annotations
from typing import Any, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorProtocol
from abdes1.core import Registry
from abdes1.core import Event, EventLoop


class ActorSystem:

    def __init__(self) -> None:
        self.registry = Registry()
        self._event_loop = EventLoop(self)
        print("Actor system created")

    # --- Registry

    def register_actor(self, actor_class: Type[ActorProtocol], *args: Any, **kwargs: Any) -> None:
        kwargs.update({'actor_system': self})
        actor = actor_class(*args, **kwargs)
        self.registry.actors.append(actor)
        print(f"Actor {actor.id} registered")

    def actor(self, actor_id: str) -> Optional[ActorProtocol]:
        return self.registry.find_actor(actor_id)

    def list_actors(self) -> List[ActorProtocol]:
        return self.registry.actors

    def find_actor(self, target_actor: str) -> Optional[ActorProtocol]:
        return self.registry.find_actor(target_actor)

    # --- Scheduler / Event loop

    def schedule_event(self, event: Event) -> None:
        self._event_loop.schedule_event(event)

    @property
    def event_loop(self) -> EventLoop:
        return self._event_loop
