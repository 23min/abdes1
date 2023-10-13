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
random.seed(333)

# Simulation variables
current_time = 0
server_busy = False
event_queue: PriorityQueue[Tuple[float, str]] = PriorityQueue()
waiting_queue: Queue[float] = Queue()


def schedule_event(event_type: str, time: float):
    event_queue.put((time, event_type))


def next_exponential(rate: float) -> float:
    return -1 / rate * (log(1.0 - random.random()))


def handle_arrival() -> None:
    global server_busy
    if not server_busy:
        server_busy = True
        schedule_event("departure", current_time + next_exponential(SERVICE_RATE))
    else:
        waiting_queue.put(current_time)

    # Schedule next arrival
    schedule_event("arrival", current_time + next_exponential(ARRIVAL_RATE))


def handle_departure() -> None:
    global server_busy
    if not waiting_queue.empty():
        waiting_queue.get()
        schedule_event("departure", current_time + next_exponential(SERVICE_RATE))
    else:
        server_busy = False


# Initialize first arrival
schedule_event("arrival", int(next_exponential(ARRIVAL_RATE)))

# Initialize time series data
time_series: List[float] = []
queue_depths: List[int] = []

# Simulation loop
for _ in range(20000):
    (current_time, event_type) = event_queue.get()
    time_series.append(current_time)
    queue_depths.append(waiting_queue.qsize())

    print(f"[{current_time:.2f}] queue depth: {waiting_queue.qsize()}")

    if event_type == "arrival":
        handle_arrival()
    else:
        handle_departure()

print(f"Average queue depth: {sum(queue_depths) / len(queue_depths)}")

# %%
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
