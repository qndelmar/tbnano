# task:fixpy-train-019
import sys
sys.path.insert(0, '.')
from mathx import km_to_miles

def main():
    print(km_to_miles(10), 'expect', 6.21371)
    print(km_to_miles(100), 'expect', 62.1371)

if __name__ == '__main__':
    main()
