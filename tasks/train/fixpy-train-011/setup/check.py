# task:fixpy-train-011
import sys
sys.path.insert(0, '.')
from helpers import moving_average

def main():
    print(moving_average((1, 2, 3, 4), 2), 'expect', [1.5, 2.5, 3.5])

if __name__ == '__main__':
    main()
