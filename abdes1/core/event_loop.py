from __future__ import annotations
from asyncio import Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorSystem, Event

from abdes1.utils import logging


class EventLoop:
    def __init__(self, verbose: bool, actor_system: ActorSystem) -> None:
        # self.actors: List[Actor] = []
        self.verbose = verbose
        self.actor_system = actor_system
        self.event_queue: Queue[Event] = Queue()
        self.current_time: float = 0.0
        logging.log_event("-loop-", "Event loop created")

    def schedule_event(self, event: Event) -> None:
        self.event_queue.put_nowait(event)

    async def run(self) -> None:
        logging.log_event("-loop-", "Event loop running")
        while True:
            event = await self.event_queue.get()

            if self.verbose:
                logging.log_event("-loop-", f"Processing event {event} with event time {event.time}")

            # TODO Improve time management
            # Advance simulation time
            if event.time > self.current_time:
                self.current_time += event.time

            if self.verbose:
                logging.log_event("-loop-", f"T: {self.current_time:>.2f}")

            # send message to actor
            target_actor = self.actor_system.find_actor(event.message.toId)
            if target_actor is not None:
                await target_actor.send_message(event.message)
            else:
                logging.log_event("-loop-", f"Error: Actor with ID {event.message.toId} not found")

        # TODO Implement Shutdown
