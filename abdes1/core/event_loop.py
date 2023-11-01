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
    actor_system: ActorSystem

    def __init__(
        self,
    ) -> None:
        self.future_event_queue: PriorityQueue[Event] = PriorityQueue()
        self.logger = ALogger("-loop-")
        self.logger.info("Event loop created")
        self.message_logger = MessageLogger("-loop-")

    def schedule_event(self, event: Event) -> None:
        self.logger.debug(f"Scheduling event {event} with scheduled time {event.time:>.2f}")
        self.future_event_queue.put_nowait(event)

    def dispatch_message(self, message: Message) -> None:
        self.logger.debug(f"Dispatching message {message} as soon as possible")
        e = Event(time=None, message=message)
        self.future_event_queue.put_nowait(e)

    async def run(self) -> None:
        self.logger.info("Event loop running")

        while True:
            event = await self.future_event_queue.get()

            self.logger.debug(f"Processing message {event.message} with scheduled time {event.time:>.2f}")

            assert event.time is not None, "message.scheduled_time is None"

            # send message to actor
            message = event.message
            target_actor = self.actor_system.find_actor(message.to_id)
            if target_actor is not None:
                message.time = event.time
                self.message_logger.log_message(event_source="-loop-", message=message)
                await target_actor.receive(message)
            else:
                self.logger.warning(f"Error: Actor '{message.to_id}' not found")

        # TODO Implement Shutdown
