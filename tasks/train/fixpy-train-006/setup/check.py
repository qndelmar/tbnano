# task:fixpy-train-006
import sys
sys.path.insert(0, '.')
from helpers import clamp

def main():
    print(clamp(5, 0, 10), 'expect', 5)
    print(clamp(15, 0, 10), 'expect', 10)

if __name__ == '__main__':
    main()
