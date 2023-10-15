from __future__ import annotations
import asyncio
from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
from abdes1.core import ActorSystem


class Actor:
    def __init__(self, id: str, actor_system: ActorSystem) -> None:
        self.id = id
        self.mailbox: Queue[Message] = Queue()
        self.actor_system = actor_system
        # self.event_loop = event_loop
        print(f"Actor {self} created")

    async def run(self) -> None:
        print(f"Actor {self.id} running")
        while True:
            message = await self.mailbox.get()
            print(f"Actor {self.id} handling mailbox message: {message}")
            if message.time > self.actor_system.event_loop.current_time:
                # Message is in the future!
                # Reschedule the message if it's too early to process it
                # TODO Can't sleep this long. The simulation time may have advanced!
                await asyncio.sleep(message.time - self.actor_system.event_loop.current_time)
            await self.process_message(message)

        # TODO support shutdown
        # print("Actor stopping")

    async def send_message(self, message: Message) -> None:
        # TODO Handle when mailbox is full / backpressure
        print(f"From actor {message.fromId}: queueing message: {message} in mailbox for {self.id}")
        await self.mailbox.put(message)

    async def process_message(self, message: Message) -> None:
        print(f"Actor {self.id} processing message: {message}")
        # TODO Implement message processing logic
        # TODO Validate message is for this actor
        # TODO Validate message format
        print(f"Actor {self.id} processed message: {message}")
        pass
