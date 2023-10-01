import asyncio

from abdes1. import Message
from abdes1.src.abdes1.core import EventLoop, Event, Message


async def main():
    event_loop = EventLoop()
    resource = Resource(event_loop, capacity=2)
    process = Process(event_loop)

    event_loop.actors.extend([resource, process])

    # Schedule an initial event
    start_message = Message(type='start', content=None, time=0.0)
    start_event = Event(time=0.0, target_actor=process, message=start_message)
    event_loop.schedule_event(start_event)

    # Start the event loop
    await event_loop.run()

    if __name__ == '__main__':
        asyncio.run(main())
