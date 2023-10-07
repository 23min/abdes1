from __future__ import annotations
import asyncio
from asyncio import Queue
from typing import TYPE_CHECKING

from abdes1.core import EventLoop
if TYPE_CHECKING:
    from .message import Message


class Actor:
    def __init__(self, id: str, event_loop: EventLoop) -> None:
        self.id = id
        self.mailbox: Queue[Message] = Queue()
        self.event_loop = event_loop
        print(f"Actor {self} created")

    async def send_message(self, fromId: str, message: Message) -> None:
        # TODO Handle when mailbox is full / backpressure
        print(f"Actor {self.id} queueing message {message} in mailbox")
        await self.mailbox.put(message)

    async def process_message(self, message: Message) -> None:
        print(f"Actor {self} processing message {message}")
        # TODO Implement message processing logic
        # TODO Validate message is for this actor
        # TODO Validate message format
        print(f"Actor {self} processed message {message}")
        pass

    async def run(self) -> None:
        print(f"Actor {self} running")
        while True:
            message = await self.mailbox.get()
            print(f"Actor {self} handling mailbox message {message}")
            if message.time > self.event_loop.simulation_time:
                # Message is in the future!
                # Reschedule the message if it's too early to process it
                await asyncio.sleep(message.time - self.event_loop.simulation_time)
            await self.process_message(message)

        # TODO support shutdown
        # print("Actor stopping")
