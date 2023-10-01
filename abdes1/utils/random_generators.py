import random


def exponential_random_variable(mean):
    return random.expovariate(1.0 / mean)
    # return -mean * random.log(random.random())


def normal_random_variable(mean, stddev):
    return random.gauss(mean, stddev)
