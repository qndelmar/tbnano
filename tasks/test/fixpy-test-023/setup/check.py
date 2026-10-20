# task:fixpy-test-023
import sys
sys.path.insert(0, '.')
from calc import sum_evens

def main():
    print(sum_evens((1, 2, 3, 4, 5, 6)), 'expect', 12)

if __name__ == '__main__':
    main()
