"""
mm1-actors.py

Implementation of an m/m/1 queueing system with actors

1. Read the confuguration from a file

    Who reads the configuraiton? The main function or the actor?
    The actor can only receive messages. So the main function should read the configuration and send it to the actor.
    Before we read from a file, try to get it to work with a hardcoded configuration.

2. Create an instance of the actor system

3. Create an instance of the queue

4. Create an instance of the server

5. What about the arrivals? A customer generator. Create an instance of the customer generator

6. Schedule an initial event to start the simulation

7. Schedule a stop event or define a stop condition

8. Run the simulation

9. Gather the metrics

10. rint the results / statistics / show the plot
"""
import asyncio
import argparse
import json

from dataclasses import asdict, dataclass
from matplotlib import pyplot as plt
from pathlib import Path
from typing import List, Optional, Tuple

from abdes1 import ActorSystem, Event, Message
from examples import LoadGeneratorActor, QueueActor, QueueType, ServerActor, StatsActor

# create a config schema
# from typing import TypedDict


@dataclass
class QueueConfig:
    id: str
    type: QueueType
    server: str


@dataclass
class ServerConfig:
    id: str
    service_rate: float


@dataclass
class LoadGeneratorConfig:
    id: str
    event_rate: float
    duration: float
    destination: str


@dataclass
class StatsConfig:
    id: str


def load_config(path: str) -> Tuple[QueueConfig, ServerConfig, LoadGeneratorConfig, StatsConfig]:
    with open(path, "r") as f:
        config_data = json.load(f)

        queue_config = QueueConfig(**config_data["queue_config"])
        server_config = ServerConfig(**config_data["server_config"])
        load_generator_config = LoadGeneratorConfig(**config_data["load_generator_config"])
        stats_config = StatsConfig(**config_data["stats_config"])

        return (queue_config, server_config, load_generator_config, stats_config)


def get_metrics() -> Tuple[list[float], List[int]]:
    time_series: List[float] = []
    queue_depths: List[int] = []
    return (time_series, queue_depths)


def plot_metrics(time_series: List[float], queue_depths: List[int]) -> None:
    # Plot the time series data
    plt.plot(  # type: ignore
        time_series,
        queue_depths,
        marker=None,
        linestyle="-",
        linewidth=0.5,
        color="black",
    )
    plt.title("M/M/1 Queue Simulation")  # type: ignore
    plt.xlabel("Time (seconds)")  # type: ignore
    plt.ylabel("Queue Depth")  # type: ignore
    plt.grid(True)  # type: ignore
    plt.tight_layout()  # type: ignore
    plt.show()  # type: ignore


async def main(config_file: Optional[str]) -> None:
    if config_file is None:
        print("Please provide a configuration file.")
        # generate configuration hardcoded instead
        queue_config = QueueConfig(
            id="queue",
            type=QueueType.FIFO,
            server="server",
        )
        server_config = ServerConfig(
            id="server",
            service_rate=1.0,
        )
        load_generator_config = LoadGeneratorConfig(
            id="arrivals",
            event_rate=1.0,
            duration=100.0,
            destination="queue",
        )
        stats_config = StatsConfig(
            id="stats",
        )
    else:
        # read the configuration from a file
        queue_config, server_config, load_generator_config, stats_config = load_config(config_file)

    # Create an instance of the actor system
    actor_system = ActorSystem()

    # Create an instance of the queue
    # kind: fifo, lifo, priority, ...
    # behaviour: blocking, non-blocking
    # actions (methods): enqueue/dequeue
    # report: queue_depth
    # optional: configure capacity
    # implementation: asyncio.Queue?
    actor_system.register_actor(QueueActor, **asdict(queue_config))

    # send a configuration message to the queue
    # queue = actor_system.get_actor("queue-1")
    # queue.send_message(Message(type="configure", content=load_config(), time=0.0))

    # Create an instance of the server
    # args = ResourceArgs(id="server-1", capacity=1)
    actor_system.register_actor(ServerActor, **asdict(server_config))
    # send a configuration message to the server
    # server = actor_system.get_actor("server-1")
    # server.send_message(Message(type="configure", content=load_config(), time=0.0))

    # Create an instance of the customer generator
    # args = ProcessArgs(id="customer-generator-1")
    actor_system.register_actor(LoadGeneratorActor, **asdict(load_generator_config))
    # send a configuration message to the customer generator
    # customer_generator = actor_system.get_actor("customer-generator-1")
    # customer_generator.send_message(Message(type="configure", content=load_config(), time=0.0))

    actor_system.register_actor(StatsActor, **asdict(stats_config))

    # Schedule an initial event 'server-ready' so that the server can start processing
    server_ready_message = Message(type="server-ready", from_id="mm1-actors", to_id="queue", content=None, time=0.0)
    server_ready_event = Event(time=0.0, message=server_ready_message)
    actor_system.schedule_event(server_ready_event)

    # Schedule an initial event to start the simulation
    start_message = Message(type="start", from_id="mm1-actors", to_id="arrivals", content=None, time=0.0)
    start_event = Event(time=0.0, message=start_message)
    actor_system.schedule_event(start_event)

    # Schedule a stop event or define a stop condition
    # after a certain time? TODO: Parametrize this
    # No, the simulation is based on duration, and the load generator will only generate customers for a certain duration
    # stop_message = Message(type="stop-simulation", content=None, time=100.0)
    # stop_event = Event(time=100.0, target_actor_id="load-generator-1", message=stop_message)
    # actor_system.schedule_event(stop_event)

    # Run the simulation
    # await asyncio.gather(actor_system.run())
    simulation_task = asyncio.create_task(actor_system.run())
    # asyncio.run(actor_system.run())

    # Gather the metrics
    # (time_series, queue_depths) = get_metrics()

    # Print the results / statistics / show the plot
    # print(f"Average queue depth: {sum(queue_depths) / len(queue_depths)}")
    # print(f"Average wait time: {sum(time_series) / len(time_series)}")
    # print(f"Average service time: {sum(time_series) / len(time_series)}")
    # plot_metrics(time_series, queue_depths)

    # Stop the simulation
    await simulation_task

    # simulation_task.cancel()

    print("Simulation completed.")


def parse_args():
    parser = argparse.ArgumentParser(description="A script that accepts a config file.")
    parser.add_argument("--config", required=False, help="Path to the configuration file.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.config and Path.exists(args.config):
        asyncio.run(main(args.config))
    else:
        print(f"File not found: {args.config}")
        asyncio.run(main(None))
