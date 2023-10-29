from __future__ import annotations
import asyncio

# from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors.message import Message
    from abdes1.core import ActorSystem
from abdes1.actors.actor import Actor

# from abdes1.core import ActorSystem
# from abdes1.utils.logger import ALogger


class DE_Actor(Actor):
    def __init__(self, id: str, actor_system: ActorSystem) -> None:
        super().__init__(id, actor_system)
        # self.logger = Logger(f"{self.id}")
        # self.logger.info(f"DE Actor '{self.id}' created")

    async def run(self) -> None:
        self.logger.info(f"Actor '{self.id}' running")
        while True:
            message = await self.mailbox.get()
            self.logger.debug(f"Handling mailbox message from '{message.from_id}': {message}. Mailbox size now [{self.mailbox.qsize()}].")

            assert message.processed is False, "Message is already processed"
            message.processed = False  # just in case
            await self.process_message(message)

    async def receive(self, message: Message) -> None:
        """
        Receive a message from another actor. Add the message to the mailbox.

        Override this method to filter or validate messages before adding them to the mailbox.

        Args:
            message (Message): _description_
        """
        # TODO Handle when mailbox is full / backpressure

        self.mailbox.put_nowait(message)
        self.logger.debug(f"Added mailbox Message from '{message.from_id}': {message}. Mailbox size now [{self.mailbox.qsize()}]. ")

        while not message.processed:
            await asyncio.sleep(0.01)
        self.logger.debug(f"Message processed: {message}")

    async def process_message(self, message: Message) -> None:
        """
        Process a message from the mailbox. Override this method to implement the actor's logic.
        """
        # print(f"DE Actor {self.id} processing message: {message}")

        # TODO Implement message processing logic
        # TODO Validate message is for this actor
        # TODO Validate message format

        # print(f"DE Actor {self.id} processed message: {message}")
        message.processed = True
