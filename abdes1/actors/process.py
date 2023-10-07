from abdes1.actors import Actor

# TODO SimPy concept. Implement this or equivalent


class Process(Actor):
    async def start(self):
        print(f'Process {self.id} started')
        pass  # Implement process start logic

    async def stop(self):
        print(f'Process {self.id} stopped')
        pass  # Implement process stop logic

    async def yield_control(self):
        print(f'Process {self.id} yielded control')
        pass  # Implement yield control logic
