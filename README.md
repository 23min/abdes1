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

[] Improve the console

Currently, the console mixes debug output and input lines. Separate the input from the output.

[] Console as an actor

Investigate whether everything can/should be an actor. The advantage if the console is an actor is that it will be easier to interact with the actor system correctly.

[] Supervisors. 

With asyncio.gather, if one of the actors crashes, it cannot be restarted. Here Erlang can be of inspiration. 

[] Implement what is needed in a DES & try to run a minimal simulation

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

[] Implement a Single Server Queueing system (M/M/1 queue)
...

[] Performance
## Q&A

Q: Why not use an existing actor framework, such as Elixir with BEAM, Akka (Pykka) etc? And why not use an existing simulation library like SimPy?

A: I was unable to find any good references on existing actor based discrete event simulation frameworks, projects or research where the two are combined.
Either it's impractical or it's genius. I'm about to find out! 
In addition, I wish to fully understand and control the simulation environment and the modeling. What better way than to create from scratch? 

