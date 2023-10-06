import asyncio
import random
from typing import Optional, cast

from abdes1.core import EventLoop, Event
from abdes1.actors import Actor, Message, Process, Resource

print("creating event loop")
event_loop = EventLoop()


def find_actor(target_actor: str) -> Optional[Actor]:
    """
    Purpose:
    """
    for actor in event_loop.actors:
        if actor.id == target_actor:
            return actor
        else:
            print(f"Actor {target_actor} not found")
            continue
    return None


# async def start_input_loop() -> None:
#     _ = asyncio.create_task(user_input_loop())
#     # The event loop is now running in the background
#     # You can do other things here, or just return
#     return


async def user_input_loop() -> None:
    while True:
        user_message: str = input("Enter your message (or 'q' to quit): ")
        if user_message.lower() == 'q':
            break

        send_after: str = input("Enter the scheduled time after which to process (seconds), enter for random:")
        if (send_after != "") and (float(send_after) < 0):
            print("Invalid time, must be positive decimal number. Try again.")
            continue

        while True:  # Loop until a valid actor is entered or user decides to break out
            target_actor = input("Enter the target actor (l to list, 'r' to reset): ")

            if target_actor.lower() == 'l':
                print("Actors:")
                for actor in event_loop.actors:
                    print(f"  {actor.id}")
                continue  # Go back to the start of the inner loop to ask for the actor again

            if target_actor.lower() == 'r':
                break  # Break out of the inner loop to start the process again
            
            actor_maybe = find_actor(target_actor)
            if actor_maybe is None:
                print(f"Actor {target_actor} not found")
                continue  # Go back to the start of the inner loop to ask for the actor again
            
            # If we reach here, we've found a valid actor, so we break out of the inner loop
            break

        # If user chooses to start over, skip the remaining logic for this iteration
        if target_actor.lower() == 'r':
            continue

        actor_maybe = find_actor(target_actor)
        if actor_maybe is None:
            print(f"Actor {target_actor} not found")
            continue

        print(f"Found Actor {target_actor}")
        actor = cast(Actor, actor_maybe)

        timestr = send_after if send_after != "" and float(send_after) else random.random() * 10
        time = cast(float, timestr)

        # time =  random.random() * cast(float, send_after)
        message = Message(type='user-message', content=user_message, time=time)

        # await actor.send_message("user", message)

        event = Event(time=time, target_actor=actor, message=message)
        event_loop.schedule_event(event)


async def main():
    # event_loop = EventLoop()
    resource = Resource("resource1", event_loop, capacity=2)
    process = Process("process1", event_loop)

    event_loop.actors.extend([resource, process])

    # Schedule an initial event
    start_message = Message(type='start-simulation', content=None, time=0.0)
    start_event = Event(time=0.0, target_actor=process, message=start_message)
    event_loop.schedule_event(start_event)

    # # Start actors
    # for actor in event_loop.actors:
    #     await actor.run()

    # # Start the event loop
    # await event_loop.run()

    # # Let the user send messages to actors
    # await start_input_loop()

    # Schedule all actors to run concurrently
    actor_tasks = [asyncio.create_task(actor.run()) for actor in event_loop.actors]

    # Schedule the event loop and input loop
    event_loop_task = asyncio.create_task(event_loop.run())
    input_loop_task = asyncio.create_task(user_input_loop())

    # Optionally, if you ever want to wait for their completion (probably not in your case, since they're endless loops)
    await asyncio.gather(*actor_tasks, event_loop_task, input_loop_task)

    pass

if __name__ == '__main__':
    asyncio.run(main())
