
# import pytest

from abdes1.actors import Actor
from abdes1.core import EventLoop


def test_actors() -> None:
    eventloop = EventLoop()
    actor1 = Actor(eventloop)
    actor2 = Actor(eventloop)

    assert actor1 in eventloop.actors
    assert actor2 in eventloop.actors
    assert len(eventloop.actors) == 2
