# import pytest

from abdes1.actors import Actor
from abdes1.core import ActorSystem, EventLoop


def test_actors() -> None:
    e = EventLoop()
    actor_system = ActorSystem(e)
    actor_system.register_actor(Actor, id="actor1")
    actor_system.register_actor(Actor, id="actor2")
    actors = actor_system.list_actors()
    actor1 = actor_system.find_actor("actor1")
    actor2 = actor_system.find_actor("actor2")
    assert actor1 in actors
    assert actor2 in actors
    assert len(actors) == 2
