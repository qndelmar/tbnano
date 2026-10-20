# task:fixpy-test-013
import sys
sys.path.insert(0, '.')
from calc import area_circle

def main():
    print(area_circle(2), 'expect', 12.56636)
    print(area_circle(5), 'expect', 78.53975)

if __name__ == '__main__':
    main()
