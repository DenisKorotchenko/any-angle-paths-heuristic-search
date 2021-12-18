from util.structures import Node


def compute_cost(i1, j1, i2, j2):
    return (abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2) ** 0.5


def make_path(goal: Node):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''

    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length


def manhattan_distance(i1, j1, i2, j2):
    return abs(int(i1) - int(i2)) + abs(int(j1) - int(j2))


def euclidian_distance(i1, j1, i2, j2):
    return ((int(i1) - int(i2)) ** 2 + (int(j1) - int(j2)) ** 2) ** 0.5
