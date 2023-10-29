from __future__ import annotations
import asyncio
from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
from abdes1.core import ActorSystem
from abdes1.utils.logger import Logger


class Actor:
    def __init__(self, id: str, actor_system: ActorSystem) -> None:
        self.id = id
        self.mailbox: Queue[Message] = Queue()
        self.actor_system = actor_system
        self.logger = Logger(f"{self.id}")
        self.logger.info(f"Actor '{self.id}' created")

    async def run(self) -> None:
        self.logger.info(f"Actor '{self.id}' running")
        while True:
            message = await self.mailbox.get()
            self.logger.debug(f"Handling mailbox message from '{message.from_id}': {message}. Mailbox size now [{self.mailbox.qsize()}].")
            # TODO: Does time have any business here?
            # if message.time > self.actor_system.event_loop.current_time:
            #     logging.log_event(self.id, f" ==> Message is in the future! {message.time} > {self.actor_system.event_loop.current_time}")
            #     # Message is in the future!
            #     # Reschedule the message if it's too early to process it
            #     # TODO Can't sleep this long. The simulation time may have advanced!
            #     await asyncio.sleep(message.time - self.actor_system.event_loop.current_time)
            # await self.receive(message)
            await self.process_message(message)
            await asyncio.sleep(0.01)

        # TODO support shutdown
        # print("Actor stopping")

    # def tell(self, message: Message, time: float) -> None:
    #     """
    #     Send a message to another actor.

    #     Args:
    #         message (Message): _description_
    #     """
    #     logging.log_event(self.id, f"Sending Message to '{message.to_id}': {message}")
    #     self.actor_system.schedule_event_from_now(Event(0.0, message))

    async def receive(self, message: Message) -> None:
        """
        Receive a message from another actor. Add the message to the mailbox.

        Override this method to filter or validate messages before adding them to the mailbox.

        Args:
            message (Message): _description_
        """
        # TODO Handle when mailbox is full / backpressure
        self.mailbox.put_nowait(message)
        self.logger.debug(f"Adding mailbox Message from '{message.from_id}': {message}. Mailbox size now [{self.mailbox.qsize()}]. ")

    async def process_message(self, message: Message) -> None:
        """
        Process a message from the mailbox. Override this method to implement the actor's logic.
        """
        print(f"Actor {self.id} processing message: {message}")
        # TODO Implement message processing logic
        # TODO Validate message is for this actor
        # TODO Validate message format
        print(f"Actor {self.id} processed message: {message}")
        pass
