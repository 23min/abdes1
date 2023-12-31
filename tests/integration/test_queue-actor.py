import pytest
import asyncio
from typing import cast

from abdes1.actors import Actor, Message
from abdes1.core import ActorSystem, Event, EventLoop
from abdes1.des import QueueActor, QueueActorArgs, QueueType

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


# @pytest.mark.asyncio
async def test_queue_can_enqueue() -> None:
    e = EventLoop()
    s = ActorSystem(e)

    # q = QueueActor(
    #     "q",
    #     "dummy-server",
    #     actor_system=s,
    # )

    s.register_actor(
        QueueActor,
        **QueueActorArgs(
            id="q",
            type=QueueType.FIFO,
            server="dummy-server",
            entity_name="customer",
        ),
    )

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(s.run())

    actors = s.list_actors()
    assert actors[0].id == "q"
    assert len(actors) == 1

    a = s.find_actor("q")
    assert a is not None
    assert a.id == "q"
    assert isinstance(a, Actor)
    q = cast(QueueActor, a)

    assert isinstance(q, Actor)
    assert isinstance(q, QueueActor)
    assert q.server == "dummy-server"

    m = Message(
        type="customer",
        from_id="pytest",
        to_id="q",
        content=None,
        time=0,
    )
    s.schedule_event(Event(time=0, message=m))
    await asyncio.sleep(1)
    assert q._get_depth() == 1  # type: ignore

    m = Message(
        type="server-ready",
        from_id="pytest",
        to_id="q",
        content=None,
        time=0,
    )
    s.schedule_event(Event(time=0, message=m))
    await asyncio.sleep(1)
    assert q._get_depth() == 0  # type: ignore

    m = Message(
        type="state",
        from_id="pytest",
        to_id="q",
        content=None,
        time=0,
    )
    s.schedule_event(Event(time=0, message=m))
    await asyncio.sleep(1)
    assert q._get_depth() == 0  # type: ignore

    m = Message(
        type="invalid message type",
        from_id="pytest",
        to_id="q",
        content=None,
        time=0,
    )
    s.schedule_event(Event(time=0, message=m))
    await asyncio.sleep(1)
    assert q._get_depth() == 0  # type: ignore
