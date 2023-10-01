from ..actors import Actor, Message


class Resource(Actor):
    def __init__(self, event_loop, capacity: int):
        super().__init__(event_loop)
        self.capacity = capacity
        self.queue = []  # A list of waiting actors

    async def request(self, actor):
        if self.capacity > 0:
            self.capacity -= 1
        else:
            self.queue.append(actor)

    async def release(self):
        if self.queue:
            await self.queue.pop(0).mailbox.put(Message(type='resource_available', content=None, time=self.event_loop.simulation_time))
        else:
            self.capacity += 1
