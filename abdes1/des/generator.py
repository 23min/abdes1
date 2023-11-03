"""
des_arrivals.py

Provides an implementation of a generator actor.

A generator actor is an actor that behaves like a source of events:
- it generates events
- it sends messages

In an m/m/1 queueing system, arrival times are exponentially distributed.
Arrival times are generated by a generator actor.
Messages are sent to the queue.

Strategy:
In a simulation, simulation time advances much more rapidly than real time.
In order to simulate events arriving at a given rate, can generate events "up front".
This is done by generating a batch of events at the start of the simulation.
"""
import random
import asyncio
from typing import Optional
from math import log


# from typing import Any, Coroutine
from abdes1.core import ActorSystem, Event
from abdes1.actors import Message
from abdes1.des import DE_Actor
from abdes1.utils.logger import ALogger


random_arrivals = random.Random()


def next_exponential(rate: float) -> float:
    return -1 / rate * (log(1.0 - random_arrivals.random()))


class Generator(DE_Actor):
    def __init__(
        self,
        id: str,
        event_rate: float,
        duration: Optional[float],
        num_arrivals: int,
        destination: str,
        entity_name: str,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.event_rate = event_rate
        self.duration = duration
        self.num_arrivals = num_arrivals
        self.destination = destination
        self.entity_name = entity_name
        self.id = id
        self.logger = ALogger(id)
        self.logger.info("Arrivals actor created")
        # TODO: Make sure the values are valid
        # event_rate should be > 0
        # duration should be > 0
        # destination should be a valid actor id

    random_arrivals.seed(333)

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    # What messages does a generator receive?
    # Start
    #    - start the generator
    #    - create a batch of arrival events?
    # Stop ? or stop condition?
    # Maybe only duration (simulated time) is enough?
    # Or the number of events generated?
    async def receive(self, message: Message) -> None:
        if message.type == "start":
            self.logger.debug("Start message received")
        await super().receive(message)

    # Generates entity: entity arrives
    # Server processes entity
    # When done, server sends message to queue "server-ready"
    async def process_message(self, message: Message) -> None:
        # based on event_rate (arrival_rate), generate a batch of events
        # How many events? numevents
        # What is the duration of the batch? duration
        # What is the time interval between events? calculated from event_rate
        # What is the time of the first event? 0
        # What is the time of the last event? duration

        # Schedule a batch of events
        scheduled_time = 0.0

        # Calculate the number of events to generate
        num_events = self.num_arrivals
        if self.duration is not None:
            num_events = int(self.event_rate * self.duration)

        last_event_time = 0.0

        # Schedule events
        for i in range(num_events):
            next_arrival_time = next_exponential(self.event_rate)
            scheduled_time += next_arrival_time
            entity = f"entity_{i}"
            event = Event(
                time=scheduled_time,
                # target_actor_id=target_actor or "",  # TODO Should be a 'deadletter' actor
                message=Message(
                    type=self.entity_name,
                    from_id=self.id,
                    to_id=self.destination,
                    content=entity,
                    time=None,
                ),
            )
            self.logger.debug(
                f"Generated arrival of '{entity}' after {next_arrival_time:.2f} at simulation time: {scheduled_time:.2f}",
            )
            self.actor_system.schedule_event(event)
            last_event_time = scheduled_time

            await asyncio.sleep(0.01)

        message.processed = True

        # Schedule a report event
        report_time = last_event_time + 10.0
        message = Message(type="save-stats", from_id="mm1-actors", to_id="stats", content=None, time=0.0)
        evt = Event(time=report_time, message=message)
        self.actor_system.schedule_event(evt)

    # --- Internal stuff
