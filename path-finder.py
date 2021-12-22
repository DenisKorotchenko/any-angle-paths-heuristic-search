import argparse
from fractions import Fraction

from algorithms.anya import anya
from algorithms.astar2k import astar2k
from algorithms.thetastar import thetastar
from draw.draw import draw
from test.movingai_util import read_map_from_movingai_file
from util.functions import euclidian_distance, make_path
from util.structures import AnyaMap, Node


def compare_step(prev2i, prev2j, previ, prevj, ci, cj):
    if cj == prevj or prev2j == prevj:
        return prevj == prev2j and cj == prevj
    return Fraction(ci - previ, cj - prevj) == Fraction(previ - prev2i, prevj - prev2j)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--astar2k", action="store_const", dest="algorithm", const=0, default=0, help="sets finding algorithm to 2^k A*, default")
    parser.add_argument("-t", "--theta", action="store_const", dest="algorithm", const=1, help="sets finding algorithm to Theta*")
    parser.add_argument("-a", "--anya", action="store_const", dest="algorithm", const=2, help="sets finding algorithm to ANYA")
    parser.add_argument("-k", action="store", dest="k", default=2, type=int, metavar="k", help="sets 2^k as limit of possible directions of moves, using in 2^k A* and Theta*, ANYA ignoring it")
    parser.add_argument("-v", "--text-output-only", action="store_true", dest="v", default=False, help="disables graphics")
    parser.add_argument("-f", "--map_file", action="store", dest="input_file", metavar="map_file", default="test/data/Moscow_0_256.map", help="filename of map")
    parser.add_argument("-i", "--task", action="store", dest="input", nargs=4, metavar=("start.i", "start.j", "goal.i", "goal.j"), type=int, help="4 integers describes the task, if None then only map will be displayed")

    args = parser.parse_args()
    if args.input_file is None:
        print("Sorry, but you need to define filename of map with -f parameter")
        return

    task_map = read_map_from_movingai_file(args.input_file, AnyaMap)
    if args.input is None:
        if not args.v:
            draw(task_map, show_in_notebook=False)
        else:
            print("Please, define task with -i parameter")
        return

    si, sj, gi, gj = args.input
    if args.algorithm == 0:
        result = astar2k(task_map, si, sj, gi, gj, euclidian_distance, k=2)
    elif args.algorithm == 1:
        result = thetastar(task_map, si, sj, gi, gj, euclidian_distance, k=2)
    elif args.algorithm == 2:
        result = anya(task_map, si, sj, gi, gj, euclidian_distance)
    else:
        assert False

    if result[0]:
        path = make_path(result[1])
        print("Path found!")
        print("Length: ", path[1])
        prev2i = -1
        prev2j = -1
        previ = -1
        prevj = -1
        print(path[0][0].i, path[0][0].j)
        for node in path[0]:
            if previ != -1 and prev2i != -1 and not compare_step(prev2i, prev2j, previ, prevj, node.i, node.j):
                print(previ, prevj)
            prev2i = previ
            prev2j = prevj
            previ = node.i
            prevj = node.j
        print(path[0][-1].i, path[0][-1].j)
        if not args.v:
            draw(task_map, start=Node(si, sj), goal=Node(gi, gj), path=path[0], show_in_notebook=False)

    else:
        print("Path not found!")
        if not args.v:
            draw(task_map, start=Node(si, sj), goal=Node(gi, gj), show_in_notebook=False)


main()