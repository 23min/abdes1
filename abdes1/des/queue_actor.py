"""
queue_actor.py

Provides an implementation of a queue actor.

A queue actor is an actor that behaves like a queue:
- it receives messages
- it sends messages
- it has a queue of messages

This queue contains entities that arrive and wait to be served by a server.

Typically, a FIFO queue is used in an m/m/1 queueing system.
In an m/m/1 queueing system, there is only one server.
The id of this server is passed to the queue actor during initialization.
"""
from asyncio import Queue

import asyncio
from typing import Optional, Tuple, TypedDict
from enum import Enum


# from typing import Any, Coroutine
from abdes1.core import ActorSystem, Event
from abdes1.actors import Message

# from abdes1.utils.logger import ALogger
from abdes1.des import DE_Actor


# Having fun with queue types. For now we only use FIFO in m/m/1
class QueueType(Enum):
    FIFO = "FIFO"
    LIFO = "LIFO"
    Priority = "Priority"
    Random = "Random"
    RoundRobin = "RoundRobin"
    SPT = "SPT"
    LPT = "LPT"
    EDD = "EDD"
    CR = "CR"


class QueueActorArgs(TypedDict):
    id: str
    type: QueueType
    server: str
    entity_name: str


class QueueActor(DE_Actor):
    def __init__(
        self,
        id: str,
        type: QueueType,
        server: str,
        entity_name: str,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.server = server
        self.entity_name = entity_name
        self.type = type
        self.queue: Queue[Tuple[float, str]] = Queue()
        self.id = id
        self.server_ready: bool = False  # keep track of server state. Used in order to keep queue_actor reentrant.

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def receive(self, message: Message) -> None:
        # TODO Validate message format
        # TODO Validate sender?
        # Validate message is for this actor

        if message.type == self.entity_name:
            self.logger.debug(f"Message received from '{message.from_id}': Entity {message.content} arrived!")
        elif message.type == "server-ready":
            self.server_ready = True
            self.logger.debug(f"Message received from '{message.from_id}': Server ready!")
        elif message.type == "get-state":
            state = f"Queue depth: {self._get_depth()}"
            print(state)  # TODO: Should really send a message back to the sender
        else:
            raise Exception(
                f"Invalid message type: {message.type}. Valid message types are: '{self.entity_name}', 'server-ready'",
            )

        await super().receive(message)

    # Arrival message: entity arrives -> enqueue
    # Server ready message: server ready ->
    #   dequeue + send message to server "serve entity"
    #
    # 1. Message "entity" received from generator.
    #    If it is the first entity and the queue is empty, send directly to server
    #    If there is a queue, enqueue message
    #    Else, if server is ready and queue is empty, send message direcetly to server
    # 2. Message "server-ready" received from server.
    #    If queue is not empty, dequeue message and send to server.
    #    If queue is empty, set server state to ready (server_ready = True)
    async def process_message(self, message: Message) -> None:
        try:
            self.logger.debug(f"Processing message: {message}")

            assert message.time is not None

            # arrival time is either the scheduled time or the time the message was sent
            arrival_time = message.time

            # If server is ready, send message directly to server
            # If server is not ready, enqueue message
            if message.type == self.entity_name:
                # If server is ready, send directly to server
                #   entity was not queued, so time == arrival_time == scheduled_time
                # Else, enqueue

                if self.server_ready:
                    if self.queue.empty():
                        self.logger.debug(f"Queue is empty. Sending {self.entity_name} '{message.content}' directly to '{self.server}'")
                        message_to_send = Message(type=self.entity_name, from_id=self.id, to_id=self.server, content=message.content)
                        self.actor_system.schedule_event(Event(time=arrival_time, message=message_to_send))
                    else:
                        # Dequeue entity and send to server
                        # Enqueue incoming message
                        # scheduled_time = time 'server-ready' was received = msessage.secheduled_time

                        self.logger.debug(
                            f"Queue is not empty. Dequeueing {self.entity_name} '{message.content}' and sending to '{self.server}'.\
                                  Queueing {self.entity_name} '{message.content}'"
                        )

                        self._enqueue(arrival_time, message.content)
                        result = await self._dequeue()
                        if result is None:
                            raise Exception("Invalid result from dequeue")

                        (_, entity) = result
                        message_to_send = Message(
                            type=self.entity_name,
                            from_id=self.id,
                            to_id=self.server,
                            content=entity,
                        )
                        self.actor_system.schedule_event(Event(time=message.time, message=message_to_send))
                else:
                    self._enqueue(arrival_time, message.content)

                self.actor_system.dispatch_message(
                    message=Message(type="queue-depth", from_id=self.id, to_id="stats", content=self.queue.qsize(), time=message.time),
                )

                self.server_ready = False

            if message.type == "server-ready":
                # The time is now the message.time, i.e. the time the message was sent from the server
                # This is equal to the dequeue time plus the service time
                # This is equal to the previous "server_ready" time plus the service time

                if (result := await self._dequeue()) is not None:
                    _, entity = result
                else:
                    # No entities in queue, but server state is ready.
                    # As soon as an entity arrives, the entity will be sent to the server
                    return

                # TODO: We can calculate the wait time here!

                self.logger.debug(f"Sending {self.entity_name} ({entity}) at the head of the queue to '{self.server}'")
                message_to_send = Message(type=self.entity_name, from_id=self.id, to_id=self.server, content=entity)

                self.actor_system.schedule_event(Event(time=message.time, message=message_to_send))
                self.server_ready = False
                self.actor_system.dispatch_message(
                    message=Message(type="queue-depth", from_id=self.id, to_id="stats", content=self.queue.qsize(), time=message.time),
                )

        finally:
            await super().process_message(message)

    # --- Internal stuff

    def _enqueue(self, arrival_time: float, entity: str) -> None:
        self.queue.put_nowait((arrival_time, entity))

    async def _dequeue(self) -> Optional[Tuple[float, str]]:
        try:
            # 0.01 is a hack to avoid the queue.get() to block forever
            async with asyncio.timeout_at(asyncio.get_running_loop().time() + 0.01):
                (arrival_time, entity) = await self.queue.get()
                self.logger.debug(f"Got '{entity}' with arrival time {arrival_time:.2f} off the queue. Queue size: {self.queue.qsize()}")
                return (arrival_time, entity)

        except TimeoutError:
            return None

    def _get_depth(self) -> int:
        return self.queue.qsize()
