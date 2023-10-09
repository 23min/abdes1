from typing import TypedDict

from abdes1.actors import Actor
from abdes1.core import ActorSystem

# TODO SimPy concept. Implement this or equivalent


class ProcessArgs(TypedDict):
    id: str


class Process(Actor):
    def __init__(self, id: str, actor_system: ActorSystem) -> None:
        super().__init__(id, actor_system)
        print(f'Process {self.id} created')

    async def start(self):
        print(f'Process {self.id} started')
        pass  # Implement process start logic

    async def stop(self):
        print(f'Process {self.id} stopped')
        pass  # Implement process stop logic

    async def yield_control(self):
        print(f'Process {self.id} yielded control')
        pass  # Implement yield control logic
