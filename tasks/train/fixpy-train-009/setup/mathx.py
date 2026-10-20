# task:fixpy-train-009
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x < hi:
        return hi
    return x
