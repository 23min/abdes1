from __future__ import annotations
from asyncio import PriorityQueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message
    from abdes1.core import ActorSystem, Event

from abdes1.utils import logging


class EventLoop:
    def __init__(self, verbose: bool, actor_system: ActorSystem) -> None:
        self.verbose = verbose
        self.actor_system = actor_system
        self.future_event_queue: PriorityQueue[Message] = PriorityQueue()
        self.current_time: float = 0.0
        logging.log_event("-loop-", "Event loop created")

    def schedule_event(self, event: Event) -> None:
        logging.log_event("-loop-", f"Scheduling event {event} with scheduled time {event.time:>.2f}")
        event.message.scheduled_time = event.time
        self.future_event_queue.put_nowait(event.message)

    def dispatch_message(self, message: Message) -> None:
        logging.log_event("-loop-", f"Dispatching message {message} as soon as possible (current time: {self.current_time}))")
        # event = Event(self.current_time, message)
        message.scheduled_time = self.current_time  # pylint: disable=used-before-assignment
        self.future_event_queue.put_nowait(message)

    async def run(self) -> None:
        logging.log_event("-loop-", "Event loop running")

        while True:
            message = await self.future_event_queue.get()

            if self.verbose:
                logging.log_event("-loop-", f"Processing message {message} with scheduled time {message.scheduled_time:>.2f}")

            assert message.scheduled_time is not None, "message.scheduled_time is None"

            # Advance simulation time
            self.current_time = message.scheduled_time

            # Advance only if the message is from actor 'queue' or actor 'server'
            # TODO: Should this be part of the configuration?
            # if (message.from_id == "queue") or (message.from_id == "server" or message.from_id == "arrivals"):
            #     if message.scheduled_time >= self.current_time:
            #         self.current_time = message.scheduled_time
            #     else:
            #         logging.log_event("-loop-", f"!!! Message scheduled_time {message.scheduled_time:>.2f} is in the past. Loop is catching up.")  # TODO: Is this a problem?

            if self.verbose:
                logging.log_event("-loop-", f"T: {self.current_time:>.2f}")

            # send message to actor
            target_actor = self.actor_system.find_actor(message.to_id)
            if target_actor is not None:
                # Update the message time to the current simulation time, i.e. the message is sent "now"
                # event.message.time = self.current_time
                message.time = self.current_time
                await target_actor.receive(message)
            else:
                logging.log_event("-loop-", f"Error: Actor '{message.to_id}' not found")

        # TODO Implement Shutdown
