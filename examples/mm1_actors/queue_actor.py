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
from typing import Optional, TypedDict
from enum import Enum


# from typing import Any, Coroutine
from abdes1.core import ActorSystem, Event
from abdes1.actors import Actor, Message


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
        self.actor_system = actor_system
        self.server = server
        self.type = type
        self.queue: Queue[str] = Queue()
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
            print(f"[{self.id:10}] Message received from {message.fromId}: Customer {message.content} arrived!")
            await self.process_message(message)
        elif message.type == "server-ready":
            self.server_ready = True
            print(f"[{self.id:10}] Message received from {message.fromId}: Server ready!")
            await self.process_message(message)
        elif message.type == "get-state":
            state = f"Queue depth: {self._get_depth()}"
            print(state)  # TODO: Should really send a message back to the sender
        else:
            raise Exception(
                f"[{self.id:10}] Invalid message type: {message.type}. \
                Valid message types are: 'customer', 'server-ready'"
            )

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
        if message.type == "customer" and not self.server_ready:
            self._enqueue(message.content)
            return

        message_to_send = None
        if message.type == "customer" and self.server_ready:
            if self.queue.empty():
                # Send directly to server
                message_to_send = Message(
                    type="customer",
                    fromId=self.id,
                    toId=self.server,
                    content=message.content,
                    time=0.0,
                )
            else:
                # Add incoming customer to queue and dequeue next customer
                self._enqueue(message.content)
                customer = await self._dequeue()
                message_to_send = Message(
                    type="customer",
                    fromId=self.id,
                    toId=self.server,
                    content=customer,
                    time=0.0,
                )

        if message.type == "server-ready" or message.content == "c_0":
            customer = await self._dequeue()

            if customer is None:
                # No customers in queue, but server state is ready.
                # As soon as a customer arrives, the customer will be sent to the sever
                # raise Exception("Server is ready, but no customers in queue. This should not happen.")
                return

            message_to_send = Message(
                type="customer",
                fromId=self.id,
                toId=self.server,
                content=customer,
                time=0.0,
            )

            # event = Event(
            #     time=0.0,
            #     message=Message(
            #         type="customer",
            #         fromId=self.id,
            #         toId=self.server,
            #         content=customer,
            #         time=0.0,
            #     ),
            # )

        self.actor_system.schedule_event(Event(time=0.0, message=message_to_send))

    # --- Internal stuff

    def _enqueue(self, customer: str) -> None:
        self.queue.put_nowait(customer)

    async def _dequeue(self) -> Optional[str]:
        # return await self.queue.get()
        print(f"Getting item of the queue. Queue size: {self.queue.qsize()}")
        try:
            async with asyncio.timeout_at(asyncio.get_running_loop().time() + 1):
                customer = await self.queue.get()
                return customer
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
