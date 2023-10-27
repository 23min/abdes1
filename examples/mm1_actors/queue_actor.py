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
        self.server_ready: bool = False  # keep track of server state. Used in order to keep queue_actor reentrant.

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def receive(self, message: Message) -> None:
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

        await super().receive(message)

    # Arrival message: customer arrives -> enqueue
    # Server ready message: server ready ->
    #   dequeue + send message to server "serve customer"
    #
    # 1. Message "customer" received from generator.
    #    If it is the first customer ('start'), send directly to server
    #    If there is a queue, enqueue message
    #    Else, if server is ready and queue is empty, send message direcetly to server
    # 2. Message "server-ready" received from server.
    #    If queue is not empty, dequeue message and send to server.
    #    If queue is empty, set server state to ready (server_ready = True)
    async def process_message(self, message: Message) -> None:
        logging.log_event(self.id, f"Processing message: {message}")

        assert message.scheduled_time is not None
        # arrival time is either the scheduled time or the time the message was sent
        self.arrival_time = message.scheduled_time

        # First customer, send directly to server
        if message.type == "customer" and message.content != "c_0":  # and not self.server_ready:
            self._enqueue(self.arrival_time, message.content)
            logging.log_event(self.id, f"Queueing customer '{message.content}'. Arrival time {self.arrival_time} Queue size: {self.queue.qsize()}")

            # Send metric to stats actor
            self.actor_system.dispatch_message(
                message=Message(type="customer-queued", from_id=self.id, to_id="stats", content=None, time=message.time, scheduled_time=None),
            )

            return

        # Second or later customer:
        #   if the queue is empty:
        #       If the server is ready: send directly to server. The shedule time is the arrival-time.
        #       Else, enqueue message.
        #   Queue is not empty, enqueue message

        # If server is ready, send message directly to server
        # If server is not ready, enqueue message

        if message.type == "customer":
            # If server is ready, send directly to server
            #   customer was not queued, so time == arrival_time == scheduled_time
            # Else, enqueue

            if self.server_ready:
                if self.queue.empty():
                    logging.log_event(self.id, f"Queue is empty. Sending customer '{message.content}' directly to '{self.server}'")
                    message_to_send = Message(
                        type="customer",
                        from_id=self.id,
                        to_id=self.server,
                        content=message.content,
                        scheduled_time=self.arrival_time,
                    )
                    self.actor_system.schedule_event(Event(0.0, message=message_to_send))
                else:
                    # Dequeue customer and send to server
                    # Enqueue incoming message
                    # scheduled_time = time 'server-ready' was received = msessage.secheduled_time

                    logging.log_event(self.id, f"Queue is not empty. Dequeueing customer '{message.content}' and sending to '{self.server}'. Queueing customer '{message.content}'")

                    self._enqueue(self.arrival_time, message.content)
                    result = await self._dequeue()
                    if result is None:
                        raise Exception("Invalid result from dequeue")

                    (_, customer) = result
                    message_to_send = Message(
                        type="customer",
                        from_id=self.id,
                        to_id=self.server,
                        content=customer,
                        scheduled_time=message.scheduled_time,
                    )
                    self.actor_system.schedule_event(Event(0.0, message=message_to_send))
            else:
                self._enqueue(self.arrival_time, message.content)
            self.server_ready = False

        if message.type == "server-ready":
            # The time is now the scheduled_time, i.e. the time the message was sent from the server
            # This is equal to the dequeue time plus the service time
            # This is equal to the previous "server_ready" time plus the service time
            # The server sent this as a schedule_event, so the time is the scheduled_time

            if (result := await self._dequeue()) is not None:
                _, customer = result
            else:
                # No customers in queue, but server state is ready.
                # As soon as a customer arrives, the customer will be sent to the server
                return

            # TODO: We can calculate the wait time here!

            logging.log_event(self.id, f"Sending in the front of the queue ({customer}) to '{self.server}'")
            message_to_send = Message(
                type="customer",
                from_id=self.id,
                to_id=self.server,
                content=customer,
                scheduled_time=message.scheduled_time,
            )

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
