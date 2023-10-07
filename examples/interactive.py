"""
interactive.py

Provides an interactivve playground for experimenting with abdes1

"""
import asyncio

# scripts findability
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from abdes1.core import EventLoop, Event
from abdes1.actors import Message, Process, Resource
from examples.console import user_input_loop


async def main():
    print("creating event loop")
    event_loop = EventLoop()

    # Define a couple of actors
    resource = Resource("resource1", event_loop, capacity=2)
    process = Process("process1", event_loop)

    event_loop.actors.extend([resource, process])

    # Schedule an initial event
    start_message = Message(type='start-simulation', content=None, time=0.0)
    start_event = Event(time=0.0, target_actor=process, message=start_message)
    event_loop.schedule_event(start_event)

    # Schedule all actors to run concurrently
    actor_tasks = [asyncio.create_task(actor.run()) for actor in event_loop.actors]

    # Schedule the future event loop
    event_loop_task = asyncio.create_task(event_loop.run())

    # Schedule the user input loop
    input_loop_task = asyncio.create_task(user_input_loop(event_loop))

    # Schedule a couple more events
    event_loop.schedule_event(Event(time=0.0,
                              target_actor=resource,
                              message=Message(type='user-message',
                                              content='hello now', time=0.0)))
    event_loop.schedule_event(Event(time=0.0,
                              target_actor=resource,
                              message=Message(type='user-message',
                                              content='hello 10s', time=10.0)))

    await asyncio.gather(*actor_tasks, event_loop_task, input_loop_task)


if __name__ == '__main__':
    asyncio.run(main())
