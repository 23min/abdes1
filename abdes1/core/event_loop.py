from __future__ import annotations
from asyncio import Queue
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Actor
    from abdes1.core import Event


class EventLoop:
    def __init__(self) -> None:
        self.actors: List[Actor] = []
        self.event_queue: Queue[Event] = Queue()
        self.simulation_time: float = 0.0
        print("Event loop created")

    def schedule_event(self, event: Event) -> None:
        self.event_queue.put_nowait(event)

    async def run(self) -> None:
        print("Event loop running")
        while True:
            event = await self.event_queue.get()
            self.simulation_time = event.time  # Advance simulation time
            await event.target_actor.mailbox.put(event.message)
