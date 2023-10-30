from __future__ import annotations
import asyncio
import time

# from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors.message import Message
    from abdes1.core import ActorSystem
from abdes1.actors.actor import Actor


class DE_Actor(Actor):
    def __init__(self, id: str, actor_system: ActorSystem) -> None:
        super().__init__(id, actor_system)

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

        timeout = 5  # or whatever value you deem appropriate
        start_time = time.time()
        while not message.processed:
            await asyncio.sleep(0.01)
            if time.time() - start_time > timeout:
                self.logger.error(f"Timeout: Message was not processed in {timeout} seconds.")
                break

        self.logger.debug(f"Message processed: {message}")

    async def process_message(self, message: Message) -> None:
        """
        Process a message from the mailbox. Override this method to implement the actor's logic.

        WAARNING: This method must be called from any subclass otherwise receive will hang
        """
        message.processed = True
