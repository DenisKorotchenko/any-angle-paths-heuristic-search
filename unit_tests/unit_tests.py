import random
from fractions import Fraction

import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

from util.functions import compute_cost
from util.structures import Map, AnyaNode, AnyaMap


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
        assert len(neighs) == 2 ** k
    print("test_get_neighbors: OK")


def test_compute_cost(eps=1e-6):
    tests = [(0, 0, 1, 1, np.sqrt(2)),
             (1, 1, 0, 0, np.sqrt(2)),
             (0, 0, 0, 10, 10),
             (0, 0, 10, 10, 10 * np.sqrt(2)),
             (0, 0, 7, 5, np.sqrt(49 + 25)),
             (0, 0, 3, 4, 5)]
    for (i1, j1, i2, j2, ans) in tests:
        assert abs(compute_cost(i1, j1, i2, j2) - ans) < eps
    print("test_compute_cost: OK")


def draw_neighbors_anya(grid_map: AnyaMap, node: AnyaNode):
    assert node is not None
    height, width = grid_map.get_size()
    k = 2048 // max(height, width)
    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color='white')
    draw = ImageDraw.Draw(im)

    for i in range(height):
        for j in range(width):
            if (not grid_map.traversable(i, j)):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

    if node.aj is None:
        neighbors = grid_map.get_start_neighbors(node.i, node.j)
    else:
        neighbors = grid_map.get_neighbors_by_node(node)
        draw.line((node.aj * k, node.ai * k, node.bj * k, node.bi * k), fill=(0, 255, 0), width=5)

    draw.ellipse((node.j * k - k / 4, node.i * k - k / 4, node.j * k + k / 4, node.i * k + k / 4), fill=(0, 255, 0), width=0)


    for neighbor in neighbors:
        color = (random.randint(0, 255), 0, random.randint(0, 255))
        print(neighbor.i, neighbor.j, neighbor.ai, neighbor.aj, neighbor.bi, neighbor.bj)
        draw.line((neighbor.aj * k, neighbor.ai * k, neighbor.bj * k, neighbor.bi * k), fill=color, width=5)
        draw.ellipse((neighbor.j * k - 10, neighbor.i * k - 10, neighbor.j * k + 10, neighbor.i * k + 10), fill=color, width=0)

    _, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(np.asarray(im))
    plt.show()


def test_neighbors_anya():
    height = 15
    width = 30
    map_str = '''
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  
. . . . . . . # # # # . # # . . . . . . . . . . . . . . . . 
. . # # # # . . . . . . . # # # # . . . . . . . . . . . . . 
. . . . . . . # # . . # . . . . . . . . . . . . . . . . . . 
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

    test_map = AnyaMap()
    test_map.read_from_string(map_str, width, height)
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(2, 2, 2, Fraction(2), 2, Fraction(6)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(3, 2, 3, Fraction(2), 3, Fraction(6)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(3, 2, 3, Fraction(2), 3, Fraction(4)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(1, 14, 1, Fraction(7), 1, Fraction(11)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(3, 17, 3, Fraction(13), 3, Fraction(17)))
    # ===== CORN NODE =====
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(5, 13, 4, Fraction(12), 4, Fraction(15)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(5, 14, 4, Fraction(12), 4, Fraction(15)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(5, 14, 3, Fraction(12), 3, Fraction(13)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(5, 10, 3, Fraction(9), 3, Fraction(11)))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(2, 13, 3, Fraction(12), 3, Fraction(13)))
    # ===== START =====
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(5, 10, None, None, None, None))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(4, 11, None, None, None, None))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(3, 12, None, None, None, None))
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(2, 13, None, None, None, None))


def test_neighbors_anya2():
    height = 15
    width = 30
    map_str = '''
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
'''
    test_map = AnyaMap()
    test_map.read_from_string(map_str, width, height)
    draw_neighbors_anya(grid_map=test_map, node=AnyaNode(14, 29, None, None, None, None))

