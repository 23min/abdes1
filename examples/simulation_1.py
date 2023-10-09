"""
simulation_1.py

Proof of concept simulation

See simulation_1.md

"""
import asyncio

from abdes1.core import ActorSystem, Event
from abdes1.actors import Message, Process, ProcessArgs, Resource, ResourceArgs
from examples.console import user_input_loop


async def main():

    print("creating actor system")
    # event_loop = EventLoop()
    actor_system = ActorSystem()

    # Define a couple of actors
    # resource = Resource("resource-1", event_loop, capacity=2)
    # process = Process("process-1", event_loop)

    args = ProcessArgs(id='process-1')
    actor_system.register_actor(type(Process), id='resource-1')

    args = ResourceArgs(id='resource-1', capacity=2)
    actor_system.register_actor(type(Resource), **args)
    # event_loop.actors.extend([resource, process])

    # Schedule an initial event
    start_message = Message(type='start-simulation', content=None, time=0.0)
    start_event = Event(time=0.0, target_actor_id='process-1', message=start_message)
    actor_system.schedule_event(start_event)

    # TODO: Refactor to Actor System and place the tasks below under supervision

    # Schedule all actors to run concurrently
    actor_tasks = [asyncio.create_task(actor.run()) for actor in actor_system.list_actors()]

    # Schedule the future event loop
    event_loop_task = asyncio.create_task(actor_system.event_loop.run())

    # Schedule the user input loop
    input_loop_task = asyncio.create_task(user_input_loop(actor_system))

    # Schedule a couple more events
    actor_system.schedule_event(
        Event(
            time=0.0,
            target_actor_id='resource-1',
            message=Message(
                type='user-message',
                content='hello now', time=0.0
            )
        )
    )
    actor_system.schedule_event(
        Event(
            time=0.0,
            target_actor_id="resource-1",
            message=Message(
                type='user-message',
                content='hello 10s', time=10.0
            )
        )
    )

    await asyncio.gather(*actor_tasks, event_loop_task, input_loop_task)


if __name__ == '__main__':
    asyncio.run(main())
