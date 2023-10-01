import asyncio
from asyncio import Queue

from .message import Message


class Actor:
    def __init__(self, event_loop):
        self.mailbox: Queue[Message] = Queue()
        self.event_loop = event_loop

    async def send_message(self, recipient: 'Actor', message: Message):
        await recipient.mailbox.put(message)

    async def process_message(self, message: Message):
        pass  # Implement message processing logic

    async def run(self):
        while True:
            message = await self.mailbox.get()
            if message.time > self.event_loop.simulation_time:
                # Reschedule the message if it's too early to process it
                await asyncio.sleep(message.time - self.event_loop.simulation_time)
            await self.process_message(message)
