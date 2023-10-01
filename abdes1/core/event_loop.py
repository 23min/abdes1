from dataclasses import dataclass
from asyncio import Queue

from ..actors import Actor, Message


@dataclass
class Event:
    time: float
    target_actor: 'Actor'
    message: Message


class EventLoop:
    def __init__(self):
        self.actors = []
        self.event_queue: Queue[Event] = Queue()
        self.simulation_time: float = 0.0

    def schedule_event(self, event: Event):
        self.event_queue.put_nowait(event)

    async def run(self):
        while True:
            event = await self.event_queue.get()
            self.simulation_time = event.time  # Advance simulation time
            await event.target_actor.mailbox.put(event)
