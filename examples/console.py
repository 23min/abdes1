import asyncio
import random
from typing import cast

from abdes1.actors import Actor, Message
from abdes1.core import EventLoop, Event


def get_user_input() -> str:
    return input("Enter your message (or 'q' to quit): ")


def get_delay() -> str:
    return input("Schedule message to number seconds from now: ")


def get_target_actor() -> str:
    return input("Enter the target actor ('l' to list, 'r' to start over, 'q' to quit): ")


async def user_input_loop(event_loop: EventLoop) -> None:
    loop = asyncio.get_running_loop()

    while True:

        user_message: str = await loop.run_in_executor(None, get_user_input)
        if user_message.lower() == 'q':
            break

        send_after: str = await loop.run_in_executor(None, get_delay)
        if (send_after != "") and (float(send_after) < 0):
            print("Invalid time, must be positive decimal number. Try again.")
            continue

        while True:  # Loop until a valid actor is entered or user decides to break out

            target_actor: str = await loop.run_in_executor(None, get_target_actor)

            if target_actor.lower() == 'l':
                print("Actors:")
                for actor in event_loop.actors:
                    print(f"  {actor.id}")
                continue  # Go back to the start of the inner loop to ask for the actor again

            if target_actor.lower() == 'r':
                break  # Break out of the inner loop to start the process again

            actor_maybe = event_loop.find_actor(target_actor)
            if actor_maybe is None:
                continue  # Go back to the start of the inner loop to ask for the actor again

            # If we reach here, we've found a valid actor, so we break out of the inner loop
            break

        # If user chooses to start over, skip the remaining logic for this iteration
        if target_actor.lower() == 'r':
            continue
        if target_actor.lower() == 'q':
            break

        print(f"Found Actor {target_actor}")
        actor = cast(Actor, actor_maybe)

        timestr = send_after if send_after != "" and float(send_after) else random.random() * 10
        time = cast(float, timestr)

        message = Message(type='user-message', content=user_message, time=time)

        event = Event(time=time, target_actor=actor, message=message)
        event_loop.schedule_event(event)

        # The rest of the user input loop...
        # When you need to interact with async code, use:
        # loop.run_until_complete(some_async_function())

        # TODO Send shutdown event
        # TODO Support shutdown in application

    print('exiting console')
