"""
interactive.py

Provides an interactivve playground for experimenting with abdes1
"""
import asyncio
from prompt_toolkit.patch_stdout import patch_stdout  # type: ignore


# scripts findability

from abdes1.core import ActorSystem, Event
from abdes1.actors import Message, Actor, Resource, ResourceArgs
from examples.console import user_input_loop


async def main():
    with patch_stdout():
        print("creating actor system")
        actor_system = ActorSystem()

        # Define a couple of actors
        actor_system.register_actor(Actor, id="actor-1")
        # Example with args (could be more complex than this!)
        args = ResourceArgs(id="resource-1", capacity=2)
        actor_system.register_actor(Resource, **args)

        # Schedule an initial event
        start_message = Message(
            type="start-simulation",
            from_id="interactive.main",
            to_id="actor-1",
            content=None,
            time=0.0,
        )
        # start_event = Event(from_id="interactive.main", time=0.0, target_actor_id="process-1", message=start_message)
        start_event = Event(time=0.0, message=start_message)
        actor_system.schedule_event(start_event)

        # Schedule the user input loop
        input_loop_task = asyncio.create_task(user_input_loop(actor_system))

        # Schedule a couple more events
        actor_system.schedule_event(
            Event(
                time=0.0,
                message=Message(
                    type="user-message",
                    from_id="interactive.main",
                    to_id="resource-1",
                    content="hello now",
                    time=0.0,
                ),
            ),
        )
        actor_system.schedule_event(
            Event(
                time=00.0,
                message=Message(
                    type="user-message",
                    from_id="interactive.main",
                    to_id="resource-1",
                    content="hello 10s",
                    time=0.0,
                ),
            ),
        )

        await asyncio.gather(actor_system.run(), input_loop_task)


if __name__ == "__main__":
    asyncio.run(main())
