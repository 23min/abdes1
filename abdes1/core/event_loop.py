from __future__ import annotations
from asyncio import PriorityQueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message
    from abdes1.core import ActorSystem

from abdes1.core import Event

from abdes1.core.message_logger import MessageLogger
from abdes1.utils.logger import ALogger


class EventLoop:
    def __init__(self, verbose: bool, actor_system: ActorSystem) -> None:
        self.verbose = verbose
        self.actor_system = actor_system
        self.future_event_queue: PriorityQueue[Event] = PriorityQueue()
        self.current_time: float = 0.0
        self.logger = ALogger("-loop-")
        self.logger.info("Event loop created")
        self.message_logger = MessageLogger("-loop-")

    def schedule_event(self, event: Event) -> None:
        self.logger.debug(f"Scheduling event {event} with scheduled time {event.time:>.2f}")
        self.future_event_queue.put_nowait(event)

    def dispatch_message(self, message: Message) -> None:
        self.logger.debug(f"Dispatching message {message} as soon as possible (current time: {self.current_time}))")
        # event = Event(self.current_time, message)
        # message.scheduled_time = self.current_time  # pylint: disable=used-before-assignment
        e = Event(time=None, message=message)
        self.future_event_queue.put_nowait(e)

    async def run(self) -> None:
        self.logger.info("Event loop running")

        while True:
            event = await self.future_event_queue.get()

            if self.verbose:
                self.logger.debug(f"Processing message {event.message} with scheduled time {event.time:>.2f}")

            assert event.time is not None, "message.scheduled_time is None"

            # Advance simulation time
            if (event.message.to_id != "stats") and (event.message.to_id != "arrivals"):
                self.current_time = event.time

            # Advance only if the message is from actor 'queue' or actor 'server'
            # TODO: Should this be part of the configuration?
            # if (message.from_id == "queue") or (message.from_id == "server" or message.from_id == "arrivals"):
            #     if message.scheduled_time >= self.current_time:
            #         self.current_time = message.scheduled_time
            #     else:
            #         logging.log_event("-loop-", f"!!! Message scheduled_time {message.scheduled_time:>.2f} is in the past. Loop is catching up.")  # TODO: Is this a problem?

            if self.verbose:
                self.logger.debug(f"T: {self.current_time:>.2f}")

            # send message to actor
            message = event.message
            target_actor = self.actor_system.find_actor(message.to_id)
            if target_actor is not None:
                # Update the message time to the current simulation time, i.e. the message is sent "now"
                # event.message.time = self.current_time
                message.time = self.current_time
                self.message_logger.log_message(event_source="-loop-", message=message)
                await target_actor.receive(message)
            else:
                self.logger.warning(f"Error: Actor '{message.to_id}' not found")

        # TODO Implement Shutdown
