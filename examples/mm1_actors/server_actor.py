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
from abdes1.actors import Actor, Message
from abdes1.utils import logging


def next_exponential(rate: float) -> float:
    return -1 / rate * (log(1.0 - random.random()))


class ServerActorArgs(TypedDict):
    id: str
    service_rate: float


class ServerActor(Actor):
    def __init__(
        self,
        id: str,
        service_rate: float,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.servce_rate = service_rate
        self.id = id

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def send_message(self, message: Message) -> None:
        # TODO Validate message format
        # TODO Validate sender?
        # Validate message is for this actor

        if message.type == "customer":
            logging.log_event(
                self.id,
                f"Message received from '{message.from_id}': Customer '{message.content}' ready to be served!",
            )
            # await self.process_message(message)
        else:
            raise Exception(
                f"Invalid message type: {message.type}. Valid message types are: 'arrival', 'server-ready'",
            )

        await super().send_message(message)

    # "customer" message: customer arrives
    # Server processes customer
    # When done, server sends message to queue "server-ready"
    async def process_message(self, message: Message) -> None:
        # Calculate random service time from service rate
        service_time = random.expovariate(self.servce_rate)

        logging.log_event(
            self.id,
            f"Customer {message.content} service time: {service_time:.2f}",
        )

        # Schedule departure event
        # The customer doesn't actually depart, he/she evaporates
        # We just send a message to the queue that the server is ready
        event = Event(
            time=service_time,
            message=Message(
                type="server-ready",
                from_id=self.id,
                to_id=message.from_id,  # TODO: Should the server be configured with the queue id?
                content=message.content,
                time=service_time,
            ),
        )

        self.actor_system.schedule_event_from_now(event)

    # --- Internal stuff
