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

## Q&A

Q: Why not use an existing actor framework, such as Elixir with BEAM, Akka (Pykka) etc? And why not use an existing simulation library like SimPy?

A: I was unable to find any good references on existing actor based discrete event simulation frameworks, projects or research where the two are combined.
Either it's impractical or it's genius. I'm about to find out! 
In addition, I wish to fully understand and control the simulation environment and the modeling. What better way than to create from scratch? 

