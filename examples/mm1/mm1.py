# %%
import random
from math import log
from queue import PriorityQueue, Queue
from typing import List, Tuple
from matplotlib import pyplot as plt

# Parameters
SERVICE_RATE = 1.8  # Average customers served per time unit
ARRIVAL_RATE = 1.8  # Average customers arriving per time unit

# Repeatable results
random_arrivals = random.Random()
random_departures = random.Random()


# Simulation variables
server_busy = False
event_queue: PriorityQueue[Tuple[float, str]] = PriorityQueue()
waiting_queue: Queue[float] = Queue()


def set_random_seeds() -> None:
    random_arrivals.seed(333)
    random_departures.seed(222)


def schedule_event(event_type: str, time: float):
    event_queue.put((time, event_type))


def next_arrival(rate: float) -> float:
    return -1 / rate * (log(1.0 - random_arrivals.random()))


def next_departure(rate: float) -> float:
    return -1 / rate * (log(1.0 - random_departures.random()))


def handle_arrival(current_time: float) -> None:
    global server_busy
    if not server_busy:
        server_busy = True
        schedule_event("departure", current_time + next_departure(SERVICE_RATE))
    else:
        waiting_queue.put(current_time)

    # Schedule next arrival
    na = current_time + next_arrival(ARRIVAL_RATE)
    schedule_event("arrival", na)
    print(f"[{current_time:.2f}] schedule arrival: {na:.2f}")


def handle_departure(current_time: float) -> None:
    global server_busy
    if not waiting_queue.empty():
        waiting_queue.get()
        nd = current_time + next_departure(SERVICE_RATE)
        schedule_event("departure", nd)
        print(f"[{current_time:.2f}] schedule departure: {nd:.2f}")

    else:
        server_busy = False


def main():
    set_random_seeds()

    # Initialize first arrival
    schedule_event("arrival", next_arrival(ARRIVAL_RATE))

    # Initialize time series data
    time_series: List[float] = []
    queue_depths: List[int] = []

    # Simulation loop
    arrivals = 1
    while arrivals < 1000 or queue_depths[-1] > 0:
        (current_time, event_type) = event_queue.get()
        time_series.append(current_time)

        print(f"[{current_time:.2f}] queue depth: {waiting_queue.qsize()}")

        if event_type == "arrival" and arrivals < 1000:
            handle_arrival(current_time)
            arrivals += 1
        else:
            handle_departure(current_time)
        queue_depths.append(waiting_queue.qsize())

    print(f"Average queue depth: {sum(queue_depths) / len(queue_depths)}")

    # Write the arrival times and queue depths to a file
    with open("mm1.csv", "w") as file:
        file.write("time,queue_depth\n")
        for i in range(len(time_series)):
            file.write(f"{time_series[i]},{queue_depths[i]}\n")

    # %%
    # Plot the time series data
    plt.title("M/M/1 Queue Simulation")  # type: ignore
    plt.xlabel("Time (seconds)")  # type: ignore
    plt.ylabel("Queue Depth")  # type: ignore
    plt.grid(True)  # type: ignore
    plt.tight_layout()  # type: ignore
    plt.plot(  # type: ignore
        time_series,
        queue_depths,
        marker=None,
        linestyle="-",
        linewidth=0.5,
        color="black",
    )
    # plt.show()  # type: ignore
    plt.savefig("queue_depth_mm1.png")  # type: ignore


if __name__ == "__main__":
    main()
