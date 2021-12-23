from unit_tests.unit_tests import draw_neighbors_anya
from util.containers import OpenAnya
from algorithms.structures import AnyaMap, AnyaNode


def anya(grid_map: AnyaMap, start_i, start_j, goal_i, goal_j, heuristic_func=None, open_type=OpenAnya, show_all=False):
    starts = grid_map.get_start_neighbors(start_i, start_j)

    OPEN = open_type()
    CLOSED = dict()
    CLOSED[(start_i, start_j)] = 0
    steps = 0
    nodes_created = 0

    for start in starts:
        nodes_created += 1
        start.update_h(goal_i, goal_j)
        OPEN.add_node(start)

    while not OPEN.is_empty():
        current = OPEN.get_best_node()
        if (current.i, current.j) in CLOSED:
            if current.g > CLOSED[(current.i, current.j)]:
                continue
        if show_all:
            draw_neighbors_anya(grid_map, current)
        steps += 1
        if current.ai == goal_i and current.aj <= goal_j <= current.bj:
            return True, AnyaNode(goal_i, goal_j, None, None, None, None, g=current.F,
                                  parent=current), steps, nodes_created, OPEN, CLOSED
        for neighbour in grid_map.get_neighbors_by_node(current):
            nodes_created += 1
            if (neighbour.i, neighbour.j) in CLOSED:
                if neighbour.g > CLOSED[(neighbour.i, neighbour.j)]:
                    continue
            CLOSED[(neighbour.i, neighbour.j)] = neighbour.g
            if neighbour.i == current.i and neighbour.j == current.j:
                neighbour.parent = current.parent
            else:
                neighbour.parent = current
            neighbour.update_h(goal_i, goal_j)
            OPEN.add_node(neighbour)
    return False, None, steps, nodes_created, OPEN, CLOSED
