(From ChatGPT)

Basic discrete-event simulation involving a queue: **The Single-Server Queueing System**.
This is a cornerstone example in the world of simulation, often referred to as the M/M/1 queue in queueing theory.

## Single-Server Queueing System:

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

### Abdes1 Implementation

#### Replicate results from mm1.py

We will strive for repeatable results that match those from mm1.py.
There `random.seed(333)` is used and there is a `next_exponential` function that provides the next random number.
These random numbers are used both for the arrival and for the departure of customers wrt the queue. But the model is failrly simplistic In a sense, he departure time is *predicted* based on the SERVICE_RATE. This is an optimization. In a model that resembles reality better, the service time would be decided, at random, inside the server. 

In the first iteration, we can try to follow the simplistic m/m/1 model from mm1.py.

At this time it is unknown whether the actor system, in it's current primitive state, has enough functionality, but we will discover (and fix that) along the way.

#### Represent the M/M/1 simulation components with actors:

##### Simulation Components

- Arrivals = actor that generates customers
- Queue = actor that contains customers 
- Server = actor that serves customers

Can we use an actor to represent a queue? 
A message received from Arrivals is a customer entering the queue (enqueue).
A message received from Server is a 'ready' message. A customer leaves the queue (a message is sent to the server that a customer wants to be served)

##### Initialize the simulation:
1. Create a configuration / setup for the simulation with actors and input/configuration.
    SERVICE_RATE = 0.8  # Average customers served per time unit
    ARRIVAL_RATE = 0.8  # Average customers arriving per time unit
2. Create the actor system and actors
    a. Arrivals: a kind of producer that generates customers based on ARRIVAL_RATE
    b. Queue: a kind of container with FIFO queue behavior
    c. Server: Receives a message (customer) and sends a message 'ready' to the queue after the random service time (based on SERVICE_RATE)
3. Run the simulation (via actor_system.Run())
    - Do we need to schedule a "stop" message
4. Show the results
    - Printed output
    - Matplotlib plot


### Python Reference Implementation:

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