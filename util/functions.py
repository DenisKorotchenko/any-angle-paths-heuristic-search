from fractions import Fraction


def compute_cost(i1, j1, i2, j2):
    return (abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2) ** 0.5


def make_path(goal):
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length


def compare_step(prev2i, prev2j, previ, prevj, ci, cj):
    if cj == prevj or prev2j == prevj:
        return prevj == prev2j and cj == prevj
    return Fraction(ci - previ, cj - prevj) == Fraction(previ - prev2i, prevj - prev2j)


def check_correcting_and_optimality(goal, task_map):
    current = goal
    prev2i = -1
    prev2j = -1
    previ = -1
    prevj = -1
    while current.parent:
        if current != goal and not current.parent is None \
                and not task_map.is_obstacle(current.i, current.j) and not task_map.is_obstacle(current.i - 1, current.j) \
                and not task_map.is_obstacle(current.i, current.j - 1) and not task_map.is_obstacle(current.i - 1, current.j - 1) \
                and previ != -1 and prev2i != -1 and not compare_step(prev2i, prev2j, previ, prevj, current.i, current.j):
            print(current.i, current.j, "is not corner")
            return False
        if not task_map.traversable_step_long(current.i, current.j, current.parent.i, current.parent.j):
            print("Can't traverse from", current.parent.i, current.parent.j, " to ", current.i, current.j)
            return False
        prev2i = previ
        prev2j = prevj
        previ = current.i
        prevj = current.j
        current = current.parent
    return True


def manhattan_distance(i1, j1, i2, j2):
    return abs(int(i1) - int(i2)) + abs(int(j1) - int(j2))


def euclidian_distance(i1, j1, i2, j2):
    return ((int(i1) - int(i2)) ** 2 + (int(j1) - int(j2)) ** 2) ** 0.5
