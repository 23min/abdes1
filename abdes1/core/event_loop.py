from __future__ import annotations
from asyncio import PriorityQueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.core import ActorSystem, Event

from abdes1.utils import logging


# def compare_events(event1: Event, event2: Event) -> bool:
#     return event1.time < event2.time


class EventLoop:
    def __init__(self, verbose: bool, actor_system: ActorSystem) -> None:
        # self.actors: List[Actor] = []
        self.verbose = verbose
        self.actor_system = actor_system
        self.event_queue: PriorityQueue[Event] = PriorityQueue()
        self.current_time: float = 0.0
        logging.log_event("-loop-", "Event loop created")

    def schedule_event(self, event: Event) -> None:
        logging.log_event("-loop-", f"Scheduling event {event} with scheduled time {event.time:>.2f}")
        self.event_queue.put_nowait(event)

    def schedule_event_from_now(self, event: Event) -> None:
        logging.log_event("-loop-", f"Scheduling event {event} with scheduled time {event.time:>.2f} ({event.time} from current time)")
        event.time = self.current_time + event.time
        self.event_queue.put_nowait(event)

    async def run(self) -> None:
        logging.log_event("-loop-", "Event loop running")

        while True:
            event = await self.event_queue.get()

            if self.verbose:
                logging.log_event("-loop-", f"Processing event {event} with scheduled time {event.time:>.2f}")

            # Advance simulation time
            # Advance only if the message is from actor 'queue' or actor 'server'
            # TODO: Should this be part of the configuration?
            if (event.message.fromId == "queue") or (event.message.fromId == "server"):
                if event.time > self.current_time:
                    self.current_time = event.time
                else:
                    logging.log_event("-loop-", f"!!! Event time {event.time:>.2f} is in the past. Loop is catching up.")  # TODO: Is this a problem?

            if self.verbose:
                logging.log_event("-loop-", f"T: {self.current_time:>.2f}")

            # send message to actor
            target_actor = self.actor_system.find_actor(event.message.toId)
            if target_actor is not None:
                # Update the message time to the current simulation time, i.e. the message is sent "now"
                # event.message.time = self.current_time
                await target_actor.send_message(event.message)
            else:
                logging.log_event("-loop-", f"Error: Actor '{event.message.toId}' not found")

        # TODO Implement Shutdown
