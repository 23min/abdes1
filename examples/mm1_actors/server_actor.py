"""
server_actor.py

Provides an implementation of a server actor.

A server actor is an actor that behaves like a service:
- it receives one task at a time
- it performs the task
- it indicates to the queue that it is ready to work on the next task

In an m/m/1 queueing system, there is only one server.
"""
import random
from typing import TypedDict
from math import log

from abdes1.core import ActorSystem, Event
from abdes1.actors import Message
from abdes1.des import DE_Actor

# from abdes1.utils.logger import ALogger


def next_exponential(rate: float) -> float:
    return float(-1 / rate * (log(1.0 - random.random())))


class ServerActorArgs(TypedDict):
    id: str
    service_rate: float


class ServerActor(DE_Actor):
    def __init__(
        self,
        id: str,
        service_rate: float,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.servce_rate = service_rate
        self.id = id
        # self.logger = Logger(id)
        # self.logger.info("Server actor created")

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def receive(self, message: Message) -> None:
        # TODO Validate message format
        # TODO Validate sender?
        # Validate message is for this actor

        if message.type == "customer":
            self.logger.debug(
                f"Message received from '{message.from_id}': Customer '{message.content}' ready to be served!",
            )
            # await self.process_message(message)
        else:
            raise Exception(
                f"Invalid message type: {message.type}. Valid message types are: 'arrival', 'server-ready'",
            )

        await super().receive(message)

    # "customer" message: customer arrives
    # Server processes customer
    # When done, server schedules an event with a message "server-ready" to actor 'queue'
    async def process_message(self, message: Message) -> None:
        # Calculate random service time from service rate
        service_time = random.expovariate(self.servce_rate)

        self.logger.debug(
            f"Customer {message.content} service time: {service_time:.2f}",
        )

        if message.time is None:
            raise ValueError("Message time should have been set.")
        future_event_time = message.time + service_time

        # Schedule departure event
        # The customer doesn't actually depart, he/she evaporates
        # We just send a message to the queue that the server is ready
        # (Actually, this is a future event because all this happens instantly in the server)
        event = Event(
            time=future_event_time,
            message=Message(type="server-ready", from_id=self.id, to_id=message.from_id, content=message.content),  # TODO: Should the server be configured with the queue id?
        )

        self.actor_system.schedule_event(event)
        message.processed = True

    # --- Internal stuff
