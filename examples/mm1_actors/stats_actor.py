"""
stats_actor.py

Provides an implementation of a statistics actor.

- collect metrics from the simulation
- calculate statistics
- plot the results

Depending on the message type, it will perform certain tasks?
- "start-simulation"
- "stop-simulation"
- "customer-queued"
- "customer-dequeued"
- "server-ready"
- ?

"""
# import random
from typing import List

# from math import log

from abdes1.core import ActorSystem  # , Event
from abdes1.actors import Actor, Message

from abdes1.utils import logging


class StatsActor(Actor):
    def __init__(
        self,
        id: str,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.id = id
        self.queue_depths: List[int] = []
        self.arrival_times: List[float] = []
        self.service_times: List[float] = []
        self.wait_times: List[float] = []

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def send_message(self, message: Message) -> None:
        # TODO Validate message type and format
        # TODO Validate sender?
        # Validate message is for this actor?

        await super().send_message(message)

    # "customer" message: customer arrives
    # Server processes customer
    # When done, server sends message to queue "server-ready"
    async def process_message(self, message: Message) -> None:
        # TODO Implement message processing logic

        # Aggregate metrics
        if message.type == "customer-queued":
            logging.log_event(
                self.id,
                f"Metric received from '{message.from_id}': Customer '{message.content}' queued at {message.time}!",
            )
            self.arrival_times.append(message.time)

        # Calculate statistics

        # Plot results

        # self.actor_system.schedule_event_from_now(event)

        pass

    # --- Internal stuff
