# task:fixpy-test-001
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x < hi:
        return hi
    return x
