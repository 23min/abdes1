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
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import HTML

from abdes1.actors import Message
from abdes1.core import Event
from abdes1.core import ActorSystem

# https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1638
session = PromptSession[str]()


def get_user_input() -> str:
    return session.prompt(HTML('<aaa fg="black" bg="gold">Enter your message (or \'q\' to quit):</aaa> '))


def get_delay() -> str:
    return session.prompt(HTML('<aaa fg="black" bg="gold">Schedule message to number seconds from now:</aaa> '))


def get_target_actor() -> str:
    return session.prompt(HTML("<aaa fg=\"black\" bg=\"gold\">Enter the target actor ('l' to list, 'r' to start over, 'q' to quit):</aaa> "))


def is_float(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False


async def user_input_loop(actor_system: ActorSystem) -> None:
    loop = asyncio.get_running_loop()

    while True:
        user_message: str = await loop.run_in_executor(None, get_user_input)
        print_formatted_text(HTML(f"<gold>You entered: {user_message}</gold>"))
        if user_message.lower() == "q":
            break

        delay_s: str = await loop.run_in_executor(None, get_delay)
        if (delay_s != "") and (not is_float(delay_s) or (float(delay_s) < 0)):
            print_formatted_text(HTML("<red>Invalid time, must be positive decimal number.</red>"))
            continue
        print_formatted_text(HTML(f"<gold>You entered: {delay_s}</gold>"))

        actor_maybe = None

        while True:  # Loop until a valid actor is entered or user decides to break out
            target_actor: str = await loop.run_in_executor(None, get_target_actor)

            if target_actor.lower() == "l":
                print_formatted_text(HTML("<gold>Actors:</gold>"))

                for actor in actor_system.list_actors():
                    print_formatted_text(HTML(f"<gold>   {actor.id}</gold>"))
                continue  # Go back to the start of the inner loop to ask for the actor again

            if target_actor.lower() == "r":
                break  # Break out of the inner loop to start the process again

            actor_maybe = actor_system.find_actor(target_actor)
            if actor_maybe is None:
                print_formatted_text(HTML(f"<red>Actor {target_actor} not found</red>"))
                continue  # Go back to the start of the inner loop to ask for the actor again

            # If we reach here, we've found a valid actor, so we break out of the inner loop
            print_formatted_text(HTML(f"<gold> Found Actor {target_actor}</gold>"))
            break

        # If user chooses to start over, skip the remaining logic for this iteration
        if target_actor.lower() == "r":
            continue
        if target_actor.lower() == "q":
            break

        time = text_to_float(delay_s, lower_bound=0.0, upper_bound=10.0)
        message = Message(type="user-message", from_id="console", to_id=target_actor, content=user_message, time=time)
        event = Event(
            time=time,
            message=message,
        )
        actor_system.schedule_event(event)

        print_formatted_text(HTML(f"<cyan>Simulation time (s) {time}</cyan>"))

        # The rest of the user input loop...
        # When you need to interact with async code, use:
        # loop.run_until_complete(some_async_function())

        # TODO Send shutdown event
        # TODO Support shutdown in application

    print("exiting console")


def text_to_float(text: str, lower_bound: float = 0.0, upper_bound: float = 1.0):
    """
    Converts a text input to a float. If the conversion fails, a random float
    between the specified lower_bound and upper_bound is returned.

    Args:
    - text (str): The text input to be converted.
    - lower_bound (float): The lower bound for generating a random float.
    - upper_bound (float): The upper bound for generating a random float.

    Returns:
    - float: The converted or random float value.
    """

    try:
        return float(text)
    except ValueError:
        return random.uniform(lower_bound, upper_bound)
