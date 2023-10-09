from __future__ import annotations
from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorSystem, Event


class EventLoop:
    def __init__(self, actor_system: ActorSystem) -> None:
        # self.actors: List[Actor] = []
        self.actor_system = actor_system
        self.event_queue: Queue[Event] = Queue()
        self.simulation_time: float = 0.0
        print("Event loop created")

    def schedule_event(self, event: Event) -> None:
        self.event_queue.put_nowait(event)

    async def run(self) -> None:
        print("Event loop running")
        while True:
            event = await self.event_queue.get()
            print(f"Event loop processing event {event}")
            # TODO Improve time management
            # Advance simulation time
            if event.time > self.simulation_time:
                self.simulation_time = event.time

            # send message to actor
            target_actor = self.actor_system.find_actor(event.target_actor_id)
            if target_actor is not None:
                await target_actor.send_message("event loop. TODO: from", event.message)
            else:
                print(f"Error: Actor with ID {event.target_actor_id} not found")

        # TODO Implement Shutdown
