from asyncio import Queue
from typing import TypedDict

from abdes1.actors import Actor, Message
from abdes1.core import ActorSystem
from abdes1.core import ActorProtocol

# TODO SimPy concept. Implement Ask pattern to use this type of actor


class ResourceArgs(TypedDict):
    id: str
    capacity: int


class Resource(Actor):
    def __init__(self, id: str, capacity: int, actor_system: ActorSystem) -> None:
        super().__init__(id, actor_system)
        self.id = id
        self.capacity = capacity
        self.queue: Queue[ActorProtocol] = Queue()  # A list of waiting actors

    async def request(self, actor: ActorProtocol) -> None:
        if self.capacity > 0:
            self.capacity -= 1
        else:
            await self.queue.put(actor)

    async def release(self) -> None:
        if self.queue:
            actor = await self.queue.get()  # TODO Actors in the queue or actor Ids?
            await actor.receive(  # TODO: Need to use the schedule_message api instead
                message=Message(
                    type="resource_available",
                    from_id=self.id,
                    to_id=actor.id,
                    content=None,
                    time=0.0,
                    scheduled_time=0.0,
                ),
            )
        else:
            self.capacity += 1
