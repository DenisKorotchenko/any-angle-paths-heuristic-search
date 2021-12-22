from util.containers import Open, Closed
from util.structures import Map, Node
from util import functions as uf


def astar2k(grid_map: Map, start_i, start_j, goal_i, goal_j, heuristic_func=None, open_type=Open, closed_type=Closed, k=2):
    start_node = Node(i=start_i, j=start_j)
    OPEN = open_type()
    CLOSED = closed_type()
    steps = 0
    nodes_created = 0

    OPEN.add_node(start_node)
    while not OPEN.is_empty():
        current = OPEN.get_best_node()
        steps += 1
        if current.i == goal_i and current.j == goal_j:
            return True, current, steps, nodes_created, OPEN, CLOSED
        for (neighbour_i, neighbour_j) in grid_map.get_neighbors(current, k):
            is_left=0
            if grid_map.is_diagonal_intersection(neighbour_i, neighbour_j):
                if current.j != neighbour_j:
                    is_left = neighbour_j - current.j
                else:
                    if current.i > neighbour_i:
                        if grid_map.is_obstacle(neighbour_i, neighbour_j):
                            is_left = 1
                        else:
                            is_left = -1
                    else:
                        if grid_map.is_obstacle(neighbour_i-1, neighbour_j):
                            is_left = 1
                        else:
                            is_left = -1
            if not CLOSED.was_expanded(neighbour_i, neighbour_j, is_left):
                next_node = Node(i=neighbour_i, j=neighbour_j,
                                 g=current.g + uf.compute_cost(current.i, current.j, neighbour_i, neighbour_j),
                                 h=heuristic_func(neighbour_i, neighbour_j, goal_i, goal_j), parent=current,
                                 k=nodes_created,
                                 is_left=is_left)
                nodes_created += 1
                OPEN.add_node(next_node)
        CLOSED.add_node(current)

    return False, None, steps, nodes_created, OPEN, CLOSED
