(From ChatGPT)

Basic discrete-event simulation involving a queue: **The Single-Server Queueing System**.
This is a cornerstone example in the world of simulation, often referred to as the M/M/1 queue in queueing theory.

### Single-Server Queueing System:

#### Concept:
1. Customers arrive at a service station.
2. If the server is free, they get served immediately.
3. If the server is busy, they wait in a queue.
4. After service, the customer departs, and the next customer in line (if any) is served.

#### Key Components:
1. **Server**: Provides service to customers.
2. **Queue**: Holds waiting customers.
3. **Arrival Event**: Time at which a new customer arrives.
4. **Departure Event**: Time at which a customer finishes service and leaves.

#### Procedure:
1. Initialize the simulation: no customers, server is idle.
2. Schedule the first arrival event.
3. Process events as they occur:
   - **Arrival Event**: If the server is idle, begin service and schedule a departure. If the server is busy, join the queue.
   - **Departure Event**: Remove customer from the server. If the queue has customers, start serving the next one and schedule its departure. Otherwise, set server to idle.
4. Repeat until the desired simulation time or number of customers is reached.

#### Abdes1 Implementation

...  ## TODO

#### Python Reference Implementation:

```python
import random
import queue

# Parameters
SERVICE_RATE = 0.8  # Average customers served per time unit
ARRIVAL_RATE = 0.5  # Average customers arriving per time unit

# Simulation variables
current_time = 0
server_busy = False
event_queue = queue.PriorityQueue()
waiting_queue = queue.Queue()

def schedule_event(event_type, time):
    event_queue.put((time, event_type))

def next_exponential(rate):
    return -1/rate * (random.log(1.0 - random.random()))

def handle_arrival():
    global server_busy
    if not server_busy:
        server_busy = True
        schedule_event('departure', current_time + next_exponential(SERVICE_RATE))
    else:
        waiting_queue.put(current_time)

    # Schedule next arrival
    schedule_event('arrival', current_time + next_exponential(ARRIVAL_RATE))

def handle_departure():
    global server_busy
    if not waiting_queue.empty():
        waiting_queue.get()
        schedule_event('departure', current_time + next_exponential(SERVICE_RATE))
    else:
        server_busy = False

# Initialize first arrival
schedule_event('arrival', next_exponential(ARRIVAL_RATE))

# Simulation loop
for _ in range(100):  # Simulate 100 events
    current_time, event_type = event_queue.get()
    if event_type == 'arrival':
        handle_arrival()
    else:
        handle_departure()

print("Number of customers in queue:", waiting_queue.qsize())
```

This is a very basic implementation, and in a real-world scenario, you might want to gather statistics, handle multiple servers, add priorities, or adjust rates. But this gives you a basic idea of a simple system involving a queue and interactions.