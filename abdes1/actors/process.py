from .actor import Actor


class Process(Actor):
    async def start(self):
        pass  # Implement process start logic

    async def stop(self):
        pass  # Implement process stop logic

    async def yield_control(self):
        pass  # Implement yield control logic
