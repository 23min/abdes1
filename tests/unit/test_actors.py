
# import pytest

from abdes1.actors import Actor
from abdes1.core import EventLoop


def test_actors() -> None:
    eventloop = EventLoop()
    actor1 = Actor("actor1", eventloop)
    actor2 = Actor("actor2", eventloop)

    assert actor1 in eventloop.actors
    assert actor2 in eventloop.actors
    assert len(eventloop.actors) == 2
