from fractions import Fraction
from util.functions import compute_cost


class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node

    You might want to add other fields, methods for Node, depending on how you prefer to implement OPEN/CLOSED further on
    '''

    def __init__(self, i, j, g=0, h=0, F=None, parent=None, k=0, is_left=0):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        self.k = k
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent
        # If node is a diagonal intersection of obstacles then we need to fix available side of it
        self.is_left=is_left

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)

    def __lt__(self, other):
        '''
        Comparison between self and other. Returns is self < other (self has higher priority).

        In this lab we limit ourselves to cardinal-only uniform-cost moves (cost = 1) and
        Manhattan distance for A*, so g, h, f-values are integers, so the comparison is straightforward
        '''
        return self.F < other.F or ((self.F == other.F) and (self.h < other.h)) \
               or ((self.F == other.F) and (self.h == other.h) and (self.k > other.k))

    def __hash__(self):
        return hash((self.i, self.j))


class Map:

    def __init__(self, k=None):
        '''
        Default constructor
        '''
        self._width = 0
        self._height = 0
        self._cells = []
        self.k = k

    def read_from_string(self, cell_str, width, height):
        '''
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
        '''
        self._width = width
        self._height = height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self._cells[i][j] = 0
                    elif c == '#':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)
                i += 1
        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def set_grid_cells(self, width, height, grid_cells):
        '''
        Initialization of map by list of cells.
        '''
        self._width = width
        self._height = height
        self._cells = grid_cells

    def is_diagonal_intersection(self, i, j):
        return (self.is_obstacle(i, j) and self.is_obstacle(i-1, j-1) and not self.is_obstacle(i-1, j) and not self.is_obstacle(i, j-1)) \
            or (self.is_obstacle(i-1, j) and self.is_obstacle(i, j-1) and not self.is_obstacle(i-1, j-1) and not self.is_obstacle(i, j))

    def is_left_node(self, node_i, node_j, parent):
        is_left = 0
        if self.is_diagonal_intersection(node_i, node_j):
            if parent.j != node_j:
                is_left = node_j - parent.j
            else:
                if parent.i > node_i:
                    if self.is_obstacle(node_i, node_j):
                        is_left = 1
                    else:
                        is_left = -1
                else:
                    if self.is_obstacle(node_i - 1, node_j):
                        is_left = 1
                    else:
                        is_left = -1
        return is_left

    def in_bounds_cells(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self._width) and (0 <= i < self._height)

    def traversable_step_long(self, i1, j1, i2, j2):
        if i2 == i1:
            if j1 > j2:
                j1, j2 = j2, j1
            for j in range(j1, j2):
                if not self.traversable_step(i1, j, i1, j+1):
                    return False
            return True

        if i1 > i2:
            i1, i2 = i2, i1
            j1, j2 = j2, j1
        d = Fraction(j2 - j1, i2 - i1)
        iprev = i1
        jprev = j1
        i = i1
        j = Fraction(j1)
        while i < i2:
            i += 1
            j += d
            if j.denominator == 1:
                if not self.traversable_step(iprev, jprev, i, j.numerator):
                    return False
                iprev = i
                jprev = j.numerator
                if i != i2:
                    if self.is_obstacle(i-1, j.numerator) and self.is_obstacle(i, j.numerator-1):
                        return False
                    if self.is_obstacle(i-1, j.numerator-1) and self.is_obstacle(i, j.numerator):
                        return False
        return True

    def traversable_step(self, i1, j1, i2, j2):
        if i1 == i2:
            if i1 == 0:
                return not self.is_obstacle(i1, min(j1, j2))
            return (not self.is_obstacle(i1 - 1, min(j1, j2))) or (not self.is_obstacle(i1, min(j1, j2)))
        if j1 == j2:
            if j1 == 0:
                return not self.is_obstacle(min(i1, i2), j1)
            return (not self.is_obstacle(min(i1, i2), j1 - 1)) or (not self.is_obstacle(min(i1, i2), j1))
        if i1 > i2:
            i1, i2 = i2, i1
            j1, j2 = j2, j1
        d = Fraction(j2 - j1, (i2 - i1))
        i = i1
        j = j1
        while i < i2:
            jl = j.__floor__()
            jr = (j+d).__floor__()
            if i == i2 - 1:
                jr = j2
            mij = min(jl, jr)
            maj = max(jl, jr)
            if (i == i1 and d < 0) or (i == i2 - 1 and d > 0):
                maj -= 1
            for j_ in range(mij, maj + 1):
                if self.is_obstacle(i, j_):
                    return False
            i += 1
            j += d
        return True

    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return not self._cells[i][j]

    def get_neighbors(self, node: Node, k=None):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 4-connected (i.e. only moves into cardinal directions are allowed)
        '''
        neighbors = []
        i = node.i
        j = node.j
        if k is None:
            k = self.k
        if k is None:
            k = 2
        delta = [[[0, 1], [1, 0], [0, -1], [-1, 0]], []]
        for ind in range(3, k + 1):
            cur = ind % 2
            delta[cur] = []
            old = (ind + 1) % 2
            for old_i in range(0, len(delta[old])):
                old_i1 = (old_i + 1) % len(delta[old])
                delta[cur].append(delta[old][old_i])
                delta[cur].append([delta[old][old_i][0] + delta[old][old_i1][0], delta[old][old_i][1] + delta[old][old_i1][1]])

        delta = delta[k % 2]

        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable_step(i, j, i + d[0], j + d[1]):  # self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        if node.is_left == 0:
            return neighbors
        answer = []
        for (i, j) in neighbors:
            if j == node.j:
                if i > node.i:
                    if (self.is_obstacle(node.i, node.j) and node.is_left == 1) or (self.is_obstacle(node.i, node.j-1) and node.is_left == -1):
                        answer.append((i, j))
                if i < node.i:
                    if (self.is_obstacle(node.i-1, node.j) and node.is_left == 1) or (self.is_obstacle(node.i-1, node.j-1) and node.is_left == -1):
                        answer.append((i, j))
            if node.j - j == node.is_left:
                answer.append((i, j))
        return answer

    def get_size(self):
        return self._height, self._width

    def in_bounds(self, i, j):
        return (0 <= j <= self._width) and (0 <= i <= self._height)

    def is_obstacle(self, i, j):
        if i < 0 or j < 0 or i >= self._height or j >= self._width:
            return True
        if type(i) is Fraction:
            i = i.__floor__()
        if type(j) is Fraction:
            j = j.__floor__()
        return self._cells[i][j]


class AnyaNode:

    def __init__(self, i: int, j: int, ai: int, aj: Fraction, bi: int, bj: Fraction, g=0, h=0, F=None, parent=None, k=0):
        if aj is not None and bj is not None:
            assert aj <= bj
        self.i: int = i
        self.j: int = j
        self.ai: int = ai
        self.aj: Fraction = aj
        self.bi: int = bi
        self.bj: Fraction = bj
        self.g = g
        self.h = h
        self.k = k
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j) and (self.ai == other.ai) and (self.aj == other.aj)\
            and (self.bi == other.bi) and (self.bj == other.bj)

    def __lt__(self, other):
        return self.F < other.F or ((self.F == other.F) and (self.h < other.h)) \
               or ((self.F == other.F) and (self.h == other.h) and (self.k > other.k))

    def __hash__(self):
        return hash((self.i, self.j, self.ai, self.aj, self.bi, self.bj))

    def update_h(self, goal_i, goal_j):
        if self.i <= self.ai <= goal_i or self.i >= self.ai >= goal_i:
            pass
        else:
            goal_i = self.ai + (self.ai - goal_i)
        if goal_i == self.i:
            self.h = min(abs(self.j - self.aj) + abs(self.aj - goal_j), abs(self.j - self.bj) + abs(self.bj - goal_j))
            self.F = self.g + self.h
            return
        cj = self.j + Fraction((goal_j - self.j) * (self.ai - self.i), goal_i - self.i)
        if self.aj <= cj <= self.bj:
            self.h = ((self.i - goal_i) ** 2 + (self.j - goal_j) ** 2) ** 0.5
        else:
            self.h = min(
                ((self.i - self.ai) ** 2 + (self.j - self.aj) ** 2) ** 0.5 + ((goal_i - self.ai) ** 2 + (goal_j - self.aj) ** 2) ** 0.5,
                ((self.i - self.bi) ** 2 + (self.j - self.bj) ** 2) ** 0.5 + ((goal_i - self.bi) ** 2 + (goal_j - self.bj) ** 2) ** 0.5
            )
        self.F = self.g + self.h
        return


class AnyaMap(Map):

    # Function that generates successors of start node
    def get_start_neighbors(self, i, j):
        start_node = None
        neighbors = []
        if not self.is_obstacle(i-1, j) or not self.is_obstacle(i, j):
            tj = j
            prev_j = j
            while self.in_bounds(i, tj+1):
                tj += 1
                if self.is_obstacle(i, tj-1) != self.is_obstacle(i, tj):
                    break
                if self.is_obstacle(i-1, tj-1) != self.is_obstacle(i-1, tj):
                    break
            if tj > prev_j:
                neighbors.append(AnyaNode(i, j, i, prev_j, i, tj, parent=start_node))
        if not self.is_obstacle(i-1, j-1) or not self.is_obstacle(i, j-1):
            tj = j
            prev_j = j
            while self.in_bounds(i, tj-1):
                tj -= 1
                if self.is_obstacle(i, tj - 1) != self.is_obstacle(i, tj):
                    break
                if self.is_obstacle(i - 1, tj - 1) != self.is_obstacle(i - 1, tj):
                    break
            if tj < prev_j:
                neighbors.append(AnyaNode(i, j, i, tj, i, prev_j, parent=start_node))

        if not self.is_obstacle(i-1, j-1) or not self.is_obstacle(i-1, j):
            aj = j
            while not self.is_obstacle(i-1, aj-1):
                aj -= 1
            bj = j
            while not self.is_obstacle(i-1, bj):
                bj += 1
            prev_j = aj
            tj = aj + 1
            while tj < bj:
                if self.is_obstacle(i-2, tj-1) != self.is_obstacle(i-2, tj):
                    if tj > prev_j:
                        neighbors.append(AnyaNode(i, j, i-1, prev_j, i-1, tj, parent=start_node))
                    prev_j = tj
                tj += 1
            if tj > prev_j:
                neighbors.append(AnyaNode(i, j, i - 1, prev_j, i - 1, tj, parent=start_node))

        if not self.is_obstacle(i, j-1) or not self.is_obstacle(i, j):
            aj = j
            while not self.is_obstacle(i, aj-1):
                aj -= 1
            bj = j
            while not self.is_obstacle(i, bj):
                bj += 1
            prev_j = aj
            tj = aj + 1
            while tj < bj:
                if self.is_obstacle(i+1, tj-1) != self.is_obstacle(i+1, tj):
                    if tj > prev_j:
                        neighbors.append(AnyaNode(i, j, i+1, prev_j, i+1, tj, parent=start_node))
                    prev_j = tj
                tj += 1
            if tj > prev_j:
                neighbors.append(AnyaNode(i, j, i+1, prev_j, i+1, tj, parent=start_node))
        return neighbors

    def assert_any_non_obstacle(self, no: AnyaNode):
        assert not self.is_obstacle(no.i - 1, no.j - 1) or not self.is_obstacle(no.i - 1, no.j) \
               or not self.is_obstacle(no.i, no.j - 1) or not self.is_obstacle(no.i, no.j)
        assert not self.is_obstacle(no.ai - 1, no.aj.__ceil__() - 1) or not self.is_obstacle(no.ai - 1, no.aj.__ceil__()) \
               or not self.is_obstacle(no.ai, no.aj.__ceil__() - 1) or not self.is_obstacle(no.ai, no.aj.__ceil__())
        assert not self.is_obstacle(no.bi - 1, no.bj.__floor__() - 1) or not self.is_obstacle(no.bi - 1, no.bj.__floor__()) \
               or not self.is_obstacle(no.bi, no.bj.__floor__() - 1) or not self.is_obstacle(no.bi, no.bj.__floor__())

    # It's main function for ANYA. It generates successors of current node
    def get_neighbors_by_node(self, node: AnyaNode):
        assert(node.ai == node.bi)
        neighbors = []

        # 1) is flat successor
        if node.i == node.ai:
            # flat successors are only available for
            assert node.bj.denominator == 1
            assert node.bj.denominator == 1

            # take more remoted endpoint from the root
            pj = node.bj.numerator
            pi = node.bi
            if abs(node.aj - node.j) > abs(node.bj - node.j):
                pj = node.aj.numerator

            if (self.is_obstacle(pi-1, pj-1) and self.is_obstacle(pi, pj)) \
                    or (self.is_obstacle(pi-1, pj) and self.is_obstacle(pi, pj-1)):
                # Can't move through adjacent diagonally
                pass
            else:
                # ===== GENERATE FLAT SUCCESSORS =======
                # We need to add only one flat successor
                if pj > node.j:
                    if not self.is_obstacle(pi-1, pj) or not self.is_obstacle(pi, pj):
                        tj = pj
                        while self.in_bounds(pi, tj+1):
                            tj += 1
                            # Condition on the corner point
                            if (self.is_obstacle(pi, tj-1) != self.is_obstacle(pi, tj)) \
                                    or (self.is_obstacle(pi-1, tj-1) != self.is_obstacle(pi-1, tj)):
                                break
                        neighbors.append(AnyaNode(node.i, node.j, pi, pj, pi, tj, g=node.g))
                        self.assert_any_non_obstacle(neighbors[-1])
                else:
                    if not self.is_obstacle(pi-1, pj-1) or not self.is_obstacle(pi, pj-1):
                        tj = pj
                        while self.in_bounds(pi, tj - 1):
                            tj -= 1
                            if (self.is_obstacle(pi, tj - 1) != self.is_obstacle(pi, tj)) or (self.is_obstacle(pi - 1, tj - 1) != self.is_obstacle(pi - 1, tj)):
                                break
                        neighbors.append(AnyaNode(node.i, node.j, pi, tj, pi, pj, g=node.g))
                        self.assert_any_non_obstacle(neighbors[-1])
                # =====================================

                # ===== GENERATE CORN SUCCESSORS ===========
                # New root will be (pi, pj)
                # We need to choose side, where will go during this generation
                if pj > node.j:
                    if self.is_obstacle(pi-1, pj-1) and not self.is_obstacle(pi-1, pj):
                        # Then go to the up
                        ti = pi-1
                        tj = pj
                        prev_j = pj
                        while self.in_bounds(ti, tj+1):
                            tj += 1
                            # Stop walking if there is an obstacle between current and new rows
                            if self.is_obstacle(ti, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, prev_j, ti, tj, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                break
                            # Split interval if there is an obstacle's condition on new row changed
                            if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, prev_j, ti, tj, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                prev_j = tj
                    if self.is_obstacle(pi, pj-1) and not self.is_obstacle(pi, pj):
                        # Same, but go to the down
                        ti = pi+1
                        tj = pj
                        prev_j = pj
                        while self.in_bounds(ti, tj+1):
                            tj += 1
                            if self.is_obstacle(ti-1, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, prev_j, ti, tj, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                break
                            if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, prev_j, ti, tj, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                prev_j = tj
                # Same, but go to the left
                else:
                    if self.is_obstacle(pi-1, pj) and not self.is_obstacle(pi-1, pj-1):
                        ti = pi-1
                        tj = pj
                        prev_j = pj
                        while self.in_bounds(ti, tj-1):
                            tj -= 1
                            if self.is_obstacle(ti, tj-1):
                                neighbors.append(AnyaNode(pi, pj, ti, tj, ti, prev_j, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                break
                            if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, tj, ti, prev_j, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                prev_j = tj
                    if self.is_obstacle(pi, pj) and not self.is_obstacle(pi, pj-1):
                        ti = pi+1
                        tj = pj
                        prev_j = pj
                        while self.in_bounds(ti, tj-1):
                            tj -= 1
                            if self.is_obstacle(ti-1, tj - 1):
                                neighbors.append(AnyaNode(pi, pj, ti, tj, ti, prev_j, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                break
                            if self.is_obstacle(ti, tj - 1) != self.is_obstacle(ti, tj):
                                neighbors.append(AnyaNode(pi, pj, ti, tj, ti, prev_j, g=node.g + compute_cost(node.i, node.j, pi, pj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                                prev_j = tj
                # ==================================

        # 2) Else we have corn node, so we need to know, in which side (up or down) we need to expand
        elif node.ai < node.i:
            # Go to the top
            # Generate projection to the next row
            ti = node.ai - 1
            taj = node.j + Fraction((node.aj - node.j) * (node.i - (node.ai - 1)), (node.i - node.ai))
            tbj = node.j + Fraction((node.bj - node.j) * (node.i - (node.bi - 1)), (node.i - node.bi))
            can_make_left_turn = True
            can_make_right_turn = True

            # Our current interval can be one of two types:
            # First: when there aren't any obstacles at each cell from [a_i; b_i] between current and next rows
            # and second (we will see it later): when all of these cells are obstacles
            if not self.is_obstacle(node.ai-1, node.aj.__floor__()):
                # Firstly, we need to check that there are no obstacles on our (potential) path,
                #   if projection and current intervals don't intersect
                flag = ti >= 0
                if taj > node.bj:
                    tj = node.bj.__floor__()
                    while tj < taj:
                        if self.is_obstacle(ti, tj):
                            flag = False
                            break
                        tj += 1
                if flag and tbj < node.aj:
                    tj = node.aj.__ceil__()
                    while tj > tbj:
                        if self.is_obstacle(ti, tj-1):
                            flag = False
                            break
                        tj -= 1

                # If all is OK, we can make projection (or maybe only some part of it)
                if flag:
                    prev_j = taj
                    tj = taj.__floor__()

                    # Now we need to choose right start j (that named tj)
                    while (tj < node.aj):# or (self.is_obstacle(ti, tj) and self.in_bounds(ti, tj))):
                        if self.is_obstacle(ti, tj):
                            can_make_left_turn = False
                            prev_j = tj + 1
                        tj += 1
                    if type(prev_j) is Fraction:
                        if prev_j.denominator == 1:
                            tj = prev_j.__floor__() - 1
                        else:
                            tj = prev_j.__floor__()
                    else:
                        tj = prev_j - 1

                    # And while tj >= tbj we can project our current interval to the next row
                    while True:
                        tj += 1
                        # If we received endpoint of projection, then we need to stop circle
                        if tj >= tbj:
                            if tbj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, tbj, g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            break
                        # If there is an obstacle, then we all need to finish our projection, but also we can't
                        #   make a turn on right side (because it is not the end of projection, and we will intersect
                        #   obstacle), so we assign False to can_make_right_turn
                        if self.is_obstacle(ti, tj):
                            can_make_right_turn = False
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, tj, g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            break
                        # But if we only see how obstacle's type above us changed, we split our new interval
                        if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, Fraction(tj), g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                    # There is the end of projection
                else:
                    can_make_left_turn = False
                    can_make_right_turn = False

                # Only if left endpoint of our current interval is integer, we can turn here
                if node.aj.denominator == 1:
                    naj = node.aj.numerator
                    # Also, we need an obstacle in the left below us to turn on its corner
                    if self.is_obstacle(node.ai, naj-1):
                        # Here we try to generate flat successor in the same route as in 1)
                        if not self.is_obstacle(node.ai-1, naj-1) and not self.is_obstacle(node.ai-1, naj):
                            tj = naj
                            while self.in_bounds(node.ai, tj-1):
                                tj -= 1
                                if (self.is_obstacle(node.ai, tj - 1) != self.is_obstacle(node.ai, tj)) or (
                                        self.is_obstacle(node.ai-1, tj-1) != self.is_obstacle(node.ai-1, tj)):
                                    break
                            neighbors.append(AnyaNode(node.ai, naj, node.ai, Fraction(tj), node.ai, Fraction(naj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                            self.assert_any_non_obstacle(neighbors[-1])
                        # ====================================

                        # If we can move from left endpoint to the left endpoint of projection, then we
                        #   can try to turn and make a continuation of our projection to the left
                        if can_make_left_turn:
                            prev_j = taj
                            ti = node.ai - 1
                            tj = taj.__floor__() + 1
                            if self.is_obstacle(ti, tj-1):
                                prev_j = tj-1
                            while self.in_bounds(ti, tj-1):
                                tj -= 1
                                # If there is an obstacle between our and next rows, we can't continue
                                if self.is_obstacle(ti, tj - 1):
                                    break
                                # But if there is only changing in obstacles above next row, we just need to split interval
                                if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                                    if tj < prev_j:
                                        neighbors.append(AnyaNode(node.ai, naj, node.ai-1, Fraction(tj), node.ai-1, Fraction(prev_j), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                        self.assert_any_non_obstacle(neighbors[-1])
                                    prev_j = tj
                            if tj < prev_j:
                                neighbors.append(AnyaNode(node.ai, naj, node.ai-1, Fraction(tj), node.ai-1, Fraction(prev_j), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                        # ================================================

                # Same for right endpoint
                if node.bj.denominator == 1:
                    naj = node.bj.numerator
                    if self.is_obstacle(node.ai, naj):
                        if not self.is_obstacle(node.ai-1, naj-1) and not self.is_obstacle(node.ai-1, naj):
                            tj = naj
                            while self.in_bounds(node.ai, tj+1):
                                tj += 1
                                if (self.is_obstacle(node.ai, tj-1) != self.is_obstacle(node.ai, tj)) or (
                                        self.is_obstacle(node.ai-1, tj-1) != self.is_obstacle(node.ai-1, tj)):
                                    break
                            neighbors.append(AnyaNode(node.ai, naj, node.ai, Fraction(naj), node.ai, Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                            self.assert_any_non_obstacle(neighbors[-1])

                        if can_make_right_turn:
                            prev_j = tbj
                            ti = node.bi - 1
                            tj = tbj.__ceil__() - 1
                            if self.is_obstacle(ti, tj):
                                prev_j = tj + 1
                            while self.in_bounds(ti, tj+1):
                                tj += 1
                                if self.is_obstacle(ti, tj):
                                    break
                                if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                                    if tj > prev_j:
                                        neighbors.append(
                                            AnyaNode(node.ai, naj, node.ai-1, Fraction(prev_j), node.ai-1,
                                                     Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                        self.assert_any_non_obstacle(neighbors[-1])
                                    prev_j = tj
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.ai, naj, node.ai-1, Fraction(prev_j), node.ai-1,
                                                          Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])

            # We also need to allow cornering from left endpoint to the right and from right endpoint to the left,
            #   if there are an obstacle above our current interval
            elif (node.aj.denominator == 1 and self.is_obstacle(node.ai-1, node.aj.numerator)) or (node.bj.denominator == 1 and self.is_obstacle(node.bi-1, node.bj.numerator-1)):
                # We need to check, that we really can make these move
                # Next procedure is same with left turning etc.
                if node.aj.denominator == 1 and not self.is_obstacle(node.ai, node.aj.numerator-1):
                    naj = node.aj.numerator
                    prev_j = naj
                    ti = node.ai - 1
                    tj = prev_j + 1
                    while self.in_bounds(ti, tj-1):
                        tj -= 1
                        if self.is_obstacle(ti, tj-1):
                            break
                        if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                            if tj < prev_j:
                                neighbors.append(
                                    AnyaNode(node.ai, naj, node.ai - 1, Fraction(tj), node.ai - 1, Fraction(prev_j),
                                             g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                    if tj < prev_j:
                        neighbors.append(
                            AnyaNode(node.ai, naj, node.ai - 1, Fraction(tj), node.ai - 1, Fraction(prev_j),
                                     g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                        self.assert_any_non_obstacle(neighbors[-1])
                # Same for turn from right endpoint to the left
                if node.bj.denominator == 1 and not self.is_obstacle(node.ai, node.bj.numerator):
                    naj = node.bj.numerator
                    prev_j = naj
                    ti = node.bi - 1
                    tj = naj - 1
                    while self.in_bounds(ti, tj+1):
                        tj += 1
                        if self.is_obstacle(ti, tj):
                            break
                        if self.is_obstacle(ti-1, tj-1) != self.is_obstacle(ti-1, tj):
                            if tj > prev_j:
                                neighbors.append(
                                    AnyaNode(node.ai, naj, node.ai-1, Fraction(prev_j), node.ai-1,
                                             Fraction(tj), g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                    if tj > prev_j:
                        neighbors.append(AnyaNode(node.ai, naj, node.ai-1, Fraction(prev_j), node.ai-1,
                                                  Fraction(tj), g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                        self.assert_any_non_obstacle(neighbors[-1])

        # And now we can see last variant: corn node, but we will move to the down
        # All procedure is same with previous section
        else:
            ti = node.ai + 1
            taj = node.j + Fraction((node.aj - node.j) * (node.i - (node.ai + 1)), (node.i - node.ai))
            tbj = node.j + Fraction((node.bj - node.j) * (node.i - (node.bi + 1)), (node.i - node.bi))
            can_make_left_turn = True
            can_make_right_turn = True
            if not self.is_obstacle(node.ai, node.aj.__floor__()):
                flag = ti <= self._height
                if taj > node.bj:
                    tj = node.bj.__floor__()
                    while tj < taj:
                        if self.is_obstacle(ti-1, tj):
                            flag = False
                            break
                        tj += 1
                if flag and tbj < node.aj:
                    tj = node.aj.__ceil__()
                    while tj > tbj:
                        if self.is_obstacle(ti-1, tj-1):
                            flag = False
                            break
                        tj -= 1

                if flag:
                    prev_j = taj
                    tj = taj.__floor__()
                    while (tj < node.aj):#: or (self.is_obstacle(ti-1, tj) and self.in_bounds(ti, tj))):
                        if self.is_obstacle(ti-1, tj):
                            can_make_left_turn = False
                            prev_j = tj + 1
                        tj += 1
                    if type(prev_j) is Fraction:
                        if prev_j.denominator == 1:
                            tj = prev_j.__floor__() - 1
                        else:
                            tj = prev_j.__floor__()
                    else:
                        tj = prev_j - 1
                    while (True):
                        tj += 1
                        if tj >= tbj:
                            if tbj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, tbj, g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            break
                        if self.is_obstacle(ti-1, tj):
                            can_make_right_turn = False
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, tj, g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            break
                        if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.i, node.j, ti, prev_j, ti, Fraction(tj), g=node.g))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                else:
                    can_make_left_turn = False
                    can_make_right_turn = False

                if node.aj.denominator == 1:
                    naj = node.aj.numerator
                    if self.is_obstacle(node.ai-1, naj-1):
                        if not self.is_obstacle(node.ai, naj-1) and not self.is_obstacle(node.ai, naj):
                            tj = naj
                            while self.in_bounds(node.ai, tj-1):
                                tj -= 1
                                if (self.is_obstacle(node.ai, tj-1) != self.is_obstacle(node.ai, tj)) or (
                                        self.is_obstacle(node.ai-1, tj-1) != self.is_obstacle(node.ai - 1, tj)):
                                    break
                            neighbors.append(AnyaNode(node.ai, naj, node.ai, Fraction(tj), node.ai, Fraction(naj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                            self.assert_any_non_obstacle(neighbors[-1])
                        if can_make_left_turn:
                            prev_j = taj
                            ti = node.ai + 1
                            tj = taj.__floor__() + 1
                            if self.is_obstacle(ti-1, tj-1):
                                prev_j = tj - 1
                            while self.in_bounds(ti-1, tj-1):
                                tj -= 1
                                if self.is_obstacle(ti-1, tj-1):
                                    break
                                if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                                    if tj < prev_j:
                                        neighbors.append(AnyaNode(node.ai, naj, node.ai+1, Fraction(tj), node.ai+1,
                                                                  Fraction(prev_j),g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                        self.assert_any_non_obstacle(neighbors[-1])
                                    prev_j = tj
                            if tj < prev_j:
                                neighbors.append(
                                    AnyaNode(node.ai, naj, node.ai+1, Fraction(tj), node.ai+1, Fraction(prev_j), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])

                if node.bj.denominator == 1:
                    naj = node.bj.numerator
                    if self.is_obstacle(node.ai-1, naj):
                        if not self.is_obstacle(node.ai, naj-1) and not self.is_obstacle(node.ai, naj):
                            tj = naj
                            while self.in_bounds(node.ai+1, tj+1):
                                tj += 1
                                if (self.is_obstacle(node.ai, tj-1) != self.is_obstacle(node.ai, tj)) or (
                                        self.is_obstacle(node.ai-1, tj-1) != self.is_obstacle(node.ai-1, tj)):
                                    break
                            neighbors.append(AnyaNode(node.ai, naj, node.ai, Fraction(naj), node.ai, Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                            self.assert_any_non_obstacle(neighbors[-1])

                        if can_make_right_turn:
                            prev_j = tbj
                            ti = node.bi + 1
                            tj = tbj.__ceil__() - 1
                            if self.is_obstacle(ti-1, tj):
                                prev_j = tj + 1
                            while self.in_bounds(ti, tj+1):
                                tj += 1
                                if self.is_obstacle(ti-1, tj):
                                    break
                                if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                                    if tj > prev_j:
                                        neighbors.append(
                                            AnyaNode(node.ai, naj, node.ai+1, Fraction(prev_j), node.ai+1,
                                                     Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                        self.assert_any_non_obstacle(neighbors[-1])
                                    prev_j = tj
                            if tj > prev_j:
                                neighbors.append(AnyaNode(node.ai, naj, node.ai+1, Fraction(prev_j), node.ai+1,
                                                          Fraction(tj), g=node.g+compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])

            elif (node.aj.denominator == 1 and self.is_obstacle(node.ai, node.aj.numerator)) or (node.bj.denominator == 1 and self.is_obstacle(node.bi, node.bj.numerator-1)):
                if node.aj.denominator == 1 and not self.is_obstacle(node.ai-1, node.aj.numerator-1):
                    naj = node.aj.numerator
                    prev_j = naj
                    ti = node.ai + 1
                    tj = naj + 1
                    while self.in_bounds(ti-1, tj-1):
                        tj -= 1
                        if self.is_obstacle(ti-1, tj-1):
                            break
                        if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                            if tj < prev_j:
                                neighbors.append(AnyaNode(node.ai, naj, node.ai+1, Fraction(tj), node.ai+1,
                                                          Fraction(prev_j),
                                                          g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                    if tj < prev_j:
                        neighbors.append(
                            AnyaNode(node.ai, naj, node.ai+1, Fraction(tj), node.ai+1, Fraction(prev_j),
                                     g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                        self.assert_any_non_obstacle(neighbors[-1])
                if node.bj.denominator == 1 and not self.is_obstacle(node.ai-1, node.bj.numerator):
                    naj = node.bj.numerator
                    prev_j = naj
                    ti = node.bi + 1
                    tj = naj - 1
                    while self.in_bounds(ti, tj+1):
                        tj += 1
                        if self.is_obstacle(ti-1, tj):
                            break
                        if self.is_obstacle(ti, tj-1) != self.is_obstacle(ti, tj):
                            if tj > prev_j:
                                neighbors.append(
                                    AnyaNode(node.ai, naj, node.ai+1, Fraction(prev_j), node.ai+1,
                                             Fraction(tj), g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                                self.assert_any_non_obstacle(neighbors[-1])
                            prev_j = tj
                    if tj > prev_j:
                        neighbors.append(AnyaNode(node.ai, naj, node.ai+1, Fraction(prev_j), node.ai+1,
                                                  Fraction(tj), g=node.g + compute_cost(node.i, node.j, node.ai, naj)))
                        self.assert_any_non_obstacle(neighbors[-1])

        return neighbors
