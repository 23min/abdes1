# abdes1
## abdes1

*abdes* stands for Actor Based Discrete Event Simulation (AB + DES)

*abdes1* is the first iteration.

## Purpose

This is my first serious attempt to work with the Python ecosystem with modern Python (2023).

## Goals

1. Create a proof of concept for using an actor system for simulating a moderately complex system based on discrete events.
abdes1 is the first experiment to get a working actor model and to run a the most basic DES.
2. Learn how a moderately complex system can be modeled specifically for an actor based DES. How can the system be expressed as an input to the simulation?
3. Validate that an actor based DES provides correct results

## Non Goals

Feature parity with any other tool out there.

## Principles and Method

Simulations are performed by running an actor system which computes state over time. 
...

## TODO

[x] Improve the console

Currently, the console mixes debug output and input lines. Separate the input from the output.

[ ] Console as an actor

Investigate whether everything can/should be an actor. The advantage if the console is an actor is that it will be easier to interact with the actor system correctly.

[ ] Supervisors. 

With asyncio.gather, if one of the actors crashes, it cannot be restarted. Here Erlang can be of inspiration. 

[ ] Implement what is needed in a DES & try to run a minimal simulation (M/M/1 Single Server queueing system)

- Event calendar / Fuuture Event List / Loop
- State management / Ability to interrogate state / logging 
- Initialization / Model input / creating and starting the actor system 
    - System primitives from a declarative definition.
    - Relations 
    - Input values
- Time management / bookkeeping
- Logic & decision making / Behavior / Flow & processing of events. Actors process events but different types of events may invoke different types of behavior, etc.
- Metrics / Statistical accumulators / Logging and monitoring
- Termination conditions and implementation
- Random number genertion / how is randomness achieved or determinism guaranteed?
- GUI / Design, administration and monitoring

Also:

- Factor out all DES/simulation related code from the actor system package. The actor system should be usable as a generic actor system. Take inspiration from Ptolemy II [^1]

[ ] Misc
- Workflow/usage. Should it be a library or have a GUI (web based or native?)
- Distribution: should it be possible to scale a simulation to run on different threads/processes/nodes?


## Q&A

Q: Why not use an existing actor framework, such as Elixir with BEAM, Akka (Pykka) etc? And why not use an existing simulation library like SimPy?

A: I was unable to find any good references on existing actor based discrete event simulation frameworks, projects or research where the two are combined. (update[^1])
Either it's impractical or it's genius. I'm about to find out! 
In addition, I wish to fully understand and control the simulation environment and the modeling. What better way than to create from scratch? 

Footnote:
[^1]: Since then, I have found the [Ptolemy Project](https://ptolemy.berkeley.edu/)).

---

# Progress Notes

## 2023-11-03

abdes1 can now run a single server queue simulation (m/m/1) and get exactly the same results as loop based  reference implementation.

The reference implementation is a standalone module: `examples/mm1/mm1.py`.
The abdes1 implementation is defined in `examples/mm1_actors/mm1_actors.py`.

In order to get reproducible and comparable results, each solution must use the same random numbers.
Abdes1 uses two random number generators, one for calculating arrival times, and another one for the service times.

The reference implementation initially only used one random number generator. This was modified so the reference implementation now also uses two random number generators.

Output from m/m/1 reference implementation:

![Output from m/m/1 reference implementation](assets/queue_depth_mm1.png)

Output from abdes1 implementation:

![Output from abdes1 implementation](assets/queue_depth_mm1_actors.png)