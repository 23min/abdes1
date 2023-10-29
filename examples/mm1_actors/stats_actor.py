"""
stats_actor.py

Provides an implementation of a statistics actor.

- collect metrics from the simulation
- calculate statistics
- plot the results

Depending on the message type, it will perform certain tasks?
- "start-simulation"
- "stop-simulation"
- "customer-queued"
- "customer-dequeued"
- "server-ready"
- ?

"""
# import random
from typing import List
import matplotlib.pyplot as plt

# from math import log

from abdes1.core import ActorSystem  # , Event
from abdes1.actors import Actor, Message

from abdes1.utils.logger import Logger

# from abdes1.core.logger import log_message as log


class StatsActor(Actor):
    def __init__(
        self,
        id: str,
        output_path: str,
        actor_system: ActorSystem,
    ) -> None:
        super().__init__(id, actor_system)
        self.id = id
        self.queue_depths: List[int] = []
        self.arrival_times: List[float] = []
        self.service_times: List[float] = []
        self.wait_times: List[float] = []
        self.output_path = output_path
        self.logger = Logger("-stats-")
        self.logger.info("Stats actor created")

    async def run(self) -> None:
        await super().run()

    # --- Override Actor medhods

    # A message is sent to this actor
    async def receive(self, message: Message) -> None:
        # TODO Validate message type and format
        # TODO Validate sender?
        # Validate message is for this actor?

        await super().receive(message)

    # "customer" message: customer arrives
    # Server processes customer
    # When done, server sends message to queue "server-ready"
    async def process_message(self, message: Message) -> None:
        # TODO Implement message processing logic

        # Aggregate metrics
        if message.type == "queue-depth":
            self.logger.debug(
                f"Metric received from '{message.from_id}': Queue depth updated at {message.time}!",
            )
            queue_depth = int(message.content if message.content is not None else 0)
            self.queue_depths.append(queue_depth)
            self.arrival_times.append(message.time if message.time is not None else 0.0)

        if message.type == "save-stats":
            self.save_stats()
            self.plot_stats()

        # Calculate statistics

        # Plot results

        # self.actor_system.schedule_event_from_now(event)

        pass

    # --- Internal stuff

    def save_stats(self) -> None:
        # TODO Implement save stats logic
        # save queue_depths to file

        # Write the arrival times and queue depths to a file
        with open("stats.txt", "w") as file:
            file.write("time,queue_depth\n")
            for i in range(len(self.arrival_times)):
                file.write(f"{self.arrival_times[i]},{self.queue_depths[i]}\n")

    def plot_stats(self) -> None:
        with open("stats.txt", "r") as file:
            lines = file.readlines()[1:]  # Skip the header line
            data = [line.strip().split(",") for line in lines]
            times = [float(row[0]) for row in data]
            depths = [int(row[1]) for row in data]

        plt.title("M/M/1 Queue Simulation (Actors)")  # type: ignore
        plt.xlabel("Time (seconds)")  # type: ignore
        plt.ylabel("Queue Depth")  # type: ignore
        plt.plot(
            times,
            depths,
            marker=None,
            linestyle="-",
            linewidth=0.5,
            color="black",
        )
        plt.savefig("queue_depth_mm1_actors.png")
