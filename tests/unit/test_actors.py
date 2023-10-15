# import pytest

from abdes1.actors import Actor
from abdes1.core import ActorSystem


def test_actors() -> None:
    actor_system = ActorSystem()
    # eventloop = EventLoop(actor_system=actor_system)
    actor1 = Actor("actor1", actor_system=actor_system)
    actor2 = Actor("actor2", actor_system=actor_system)

    actors = actor_system.list_actors()
    assert actor1 in actors
    assert actor2 in actors
    assert len(actors) == 2
