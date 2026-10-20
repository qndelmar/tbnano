# task:fixpy-train-000
import sys
sys.path.insert(0, '.')
from compute import km_to_miles

def main():
    print(km_to_miles(10), 'expect', 6.21371)
    print(km_to_miles(100), 'expect', 62.1371)

if __name__ == '__main__':
    main()
