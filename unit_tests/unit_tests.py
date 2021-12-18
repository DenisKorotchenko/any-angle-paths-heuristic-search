import numpy as np

from util.functions import compute_cost
from util.structures import Map

def test_get_neighbors():
    height = 15
    width = 30
    map_str = '''
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
'''

    test_map = Map()
    test_map.read_from_string(map_str, width, height)

    neighs = test_map.get_neighbors(9, 18, 5)
    for i in range(height):
        s = ""
        for j in range(width):
            if (i, j) in neighs:
                s += "# "
            else:
                s += ". "
        print(s)
    for k in range(2, 7):
        neighs = test_map.get_neighbors(7, 7, k)
        assert len(neighs) == 2**k
    print("test_get_neighbors: OK")




def test_compute_cost(eps = 1e-6):
    tests = [(0, 0, 1, 1, np.sqrt(2)),
             (1, 1, 0, 0, np.sqrt(2)),
             (0, 0, 0, 10, 10),
             (0, 0, 10, 10, 10*np.sqrt(2)),
             (0, 0, 7, 5, np.sqrt(49+25)),
             (0, 0, 3, 4, 5)]
    for (i1, j1, i2, j2, ans) in tests:
        assert abs(compute_cost(i1, j1, i2, j2) - ans) < eps
    print("test_compute_cost: OK")


test_get_neighbors()
test_compute_cost()