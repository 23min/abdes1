"""
    console.py

    Provides an interactive console with input separated from output.

    Input prompt is one line that is sticky to the bottom of the console window.

    Uses `prompt-toolkit`
    Html formatting see https://python-prompt-toolkit.readthedocs.io/en/master/pages/printing_text.html

"""
from __future__ import annotations
import asyncio
import random
from typing import cast
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import HTML

from abdes1.actors import Actor, Message
from abdes1.core import EventLoop, Event

# https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1638
session = PromptSession[str]()


def get_user_input() -> str:
    return session.prompt(HTML('<aaa fg="black" bg="gold">Enter your message (or \'q\' to quit):</aaa> '))


def get_delay() -> str:
    return session.prompt(HTML('<aaa fg="black" bg="gold">Schedule message to number seconds from now:</aaa> '))


def get_target_actor() -> str:
    return session.prompt(HTML('<aaa fg="black" bg="gold">Enter the target actor (\'l\' to list, \'r\' to start over, \'q\' to quit):</aaa> '))


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


async def user_input_loop(event_loop: EventLoop) -> None:

    loop = asyncio.get_running_loop()

    while True:

        user_message: str = await loop.run_in_executor(None, get_user_input)
        print_formatted_text(HTML(f"<gold>You entered: {user_message}</gold>"))
        if user_message.lower() == 'q':
            break

        delay_s: str = await loop.run_in_executor(None, get_delay)
        if (delay_s != "") and (not is_float(delay_s) or (float(delay_s) < 0)):
            print_formatted_text(HTML("<red>Invalid time, must be positive decimal number.</red>"))
            continue
        print_formatted_text(HTML(f"<gold>You entered: {delay_s}</gold>"))

        while True:  # Loop until a valid actor is entered or user decides to break out

            target_actor: str = await loop.run_in_executor(None, get_target_actor)

            if target_actor.lower() == 'l':
                # print("Actors:")
                print_formatted_text(HTML("<gold>Actors:</gold>"))

                for actor in event_loop.actors:
                    print_formatted_text(HTML(f"<gold>   {actor.id}</gold>"))
                    # print(f"  {actor.id}")
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

        # print(f"Found Actor {target_actor}")
        print_formatted_text(HTML(f"<gold> Found Actor {target_actor}</gold>"))
        actor = cast(Actor, actor_maybe)

        timestr = delay_s if delay_s != "" and float(delay_s) else random.random() * 10
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
