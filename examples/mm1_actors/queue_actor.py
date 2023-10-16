"""
queue_actor.py

Provides an implementation of a queue actor.

A queue actor is an actor that behaves like a queue:
- it receives messages
- it sends messages
- it has a queue of messages

This queue contains customers that arrive and wait to be served by a server.

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
from abdes1.actors import Actor, Message
from abdes1.utils import logging


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


class QueueActor(Actor):
    def __init__(
        self,
        id: str,
        type: QueueType,
        server: str,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.server = server
        self.type = type
        self.queue: Queue[Tuple[float, str]] = Queue()
        self.id = id
        self.server_ready = False  # keep track of server state. Used in order to keep queue_actor reentrant.

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def send_message(self, message: Message) -> None:
        # TODO Validate message format
        # TODO Validate sender?
        # Validate message is for this actor

        if message.type == "customer":
            logging.log_event(self.id, f"Message received from '{message.from_id}': Customer {message.content} arrived!")
        elif message.type == "server-ready":
            self.server_ready = True
            logging.log_event(self.id, f"Message received from '{message.from_id}': Server ready!")
        elif message.type == "get-state":
            state = f"Queue depth: {self._get_depth()}"
            print(state)  # TODO: Should really send a message back to the sender
        else:
            raise Exception(
                f"Invalid message type: {message.type}. Valid message types are: 'customer', 'server-ready'",
            )

        await super().send_message(message)

    # Arrival message: customer arrives -> enqueue
    # Server ready message: server ready ->
    #   dequeue + send message to server "serve customer"
    #
    # 1. Message "customer" received from generator.
    #    If server is ready, send message directly  to server.
    #    If server is not ready, enqueue message.
    # 2. Message "server-ready" received from server.
    #    If queue is not empty, dequeue message and send to server.
    #    If queue is empty, set server state to ready (server_ready = True)
    async def process_message(self, message: Message) -> None:
        logging.log_event(self.id, f"Processing message: {message}")

        if message.type == "customer" and not self.server_ready:
            self._enqueue(message.time, message.content)
            return

        message_to_send = None
        if message.type == "customer" and self.server_ready:
            if self.queue.empty():
                logging.log_event(self.id, f"Queue is empty. Sending customer '{message.content}' directly to '{self.server}'")
                message_to_send = Message(
                    type="customer",
                    from_id=self.id,
                    to_id=self.server,
                    content=message.content,
                    time=message.time,
                )
            else:
                logging.log_event(self.id, f"Queue is not empty. Dequeueing customer '{message.content}' and sending to '{self.server}'. Queueing customer '{message.content}'")
                self._enqueue(message.time, message.content)
                result = await self._dequeue()
                if result is None:
                    raise Exception("Invalid result from dequeue")
                (arrival_time, customer) = result
                message_to_send = Message(
                    type="customer",
                    from_id=self.id,
                    to_id=self.server,
                    content=customer,
                    time=arrival_time,
                )

        if message.type == "server-ready":  # or message.content == "c_0":
            result = await self._dequeue()
            if result is None:
                # No customers in queue, but server state is ready.
                # As soon as a customer arrives, the customer will be sent to the sever
                return
            (arrival_time, customer) = result

            logging.log_event(self.id, f"Sending first customer in the queue ({customer}) to '{self.server}'")
            message_to_send = Message(
                type="customer",
                from_id=self.id,
                to_id=self.server,
                content=customer,
                time=arrival_time,
            )

        if message_to_send is not None:
            self.actor_system.schedule_event_from_now(Event(0.0, message=message_to_send))
        else:
            raise Exception("Invalid message type.")

    # --- Internal stuff

    def _enqueue(self, arrival_time: float, customer: str) -> None:
        self.queue.put_nowait((arrival_time, customer))

    async def _dequeue(self) -> Optional[Tuple[float, str]]:
        # return await self.queue.get()
        try:
            # 0.01 is a hack to avoid the queue.get() to block forever
            async with asyncio.timeout_at(asyncio.get_running_loop().time() + 0.01):
                (arrival_time, customer) = await self.queue.get()
                logging.log_event(self.id, f"Got '{customer}' with arrival time {arrival_time:.2f} off the queue. Queue size: {self.queue.qsize()}")
                return (arrival_time, customer)
            # return await asyncio.wait_for(self.queue.get(), timeout=1)
            # print(f"[{self.id}] Message received from {message.fromId}: Serving customer {customer}...")
            # if self.last_server_message is not None:
            # await self.actor_system.send_message(Message(self.id, self.last_server_message, customer))

        except TimeoutError:
            # print(f"[{self.id}] Message received from {message.fromId}: No customers in queue.")
            # if self.last_server_message is not None:
            #     await self.actor_system.send_message(Message(self.id, self.last_server_message, None))
            return None

    def _get_depth(self) -> int:
        return self.queue.qsize()
