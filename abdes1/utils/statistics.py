def mean(values):
    return sum(values) / len(values) if values else 0

def variance(values):
    m = mean(values)
    return sum((x - m) ** 2 for x in values) / len(values) if values else 0
