
from asyncio import Queue
# from typing import TYPE_CHECKING

from abdes1.actors import Actor, Message
from abdes1.core import EventLoop
# if TYPE_CHECKING:

# TODO SimPy concept. Implement Ask pattern to use this type of actor


class Resource(Actor):
    def __init__(self, id: str, event_loop: EventLoop, capacity: int) -> None:
        super().__init__(id, event_loop)
        self.capacity = capacity
        self.queue: Queue[Actor] = Queue()  # A list of waiting actors

    async def request(self, actor: Actor) -> None:
        if self.capacity > 0:
            self.capacity -= 1
        else:
            await self.queue.put(actor)

    async def release(self) -> None:
        if self.queue:
            actor = await self.queue.get()
            await actor.mailbox.put(
                Message(type='resource_available', content=None, time=self.event_loop.simulation_time)
            )
        else:
            self.capacity += 1
