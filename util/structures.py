class Map:

    def __init__(self, k = None):
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
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                i += 1
        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )
    
     
    def set_grid_cells(self, width, height, grid_cells):
        '''
        Initialization of map by list of cells.
        '''
        self._width = width
        self._height = height
        self._cells = grid_cells


    def in_bounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self._width) and (0 <= i < self._height)
    

    def traversable_step(self, i1, j1, i2, j2, eps = 1e-9):
        if i1 == i2:
            if i1 == 0:
                return (not self._cells[i1][min(j1, j2)])
            return (not self._cells[i1-1][min(j1, j2)]) or (not self._cells[i1][min(j1, j2)])
        if j1 == j2:
            if j1 == 0:
                return (not self._cells[min(i1, i2)][j1])
            return (not self._cells[min(i1, i2)][j1-1]) or (not self._cells[min(i1, i2)][j1])
        if i1 > i2:
            i1, i2 = i2, i1
            j1, j2 = j2, j1
        d = (j2 - j1) / (i2 - i1)
        i = i1
        j = j1
        while i < i2:
            jl = int(j)
            jr = int(j + d)
            if (i == i2-1):
                jr = j2
            mij = min(jl, jr)
            maj = max(jl, jr)
            if (i == i1 and d < 0) or (i == i2-1 and d > 0):
                maj -= 1
            for j_ in range(mij, maj+1):
                if self._cells[i][j_]:
                    return False
            i += 1
            j += d
        return True
        
    
    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return not self._cells[i][j]


    def get_neighbors(self, i, j, k = None):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 4-connected (i.e. only moves into cardinal directions are allowed)
        '''   
        neighbors = []
        if k is None:
            k = self.k
        if k is None:
            k = 2
        delta = [[[0, 1], [1, 0], [0, -1], [-1, 0]], []]
        for ind in range(3, k+1):
            cur = ind % 2
            delta[cur] = []
            old = (ind + 1) % 2
            for old_i in range(0, len(delta[old])):
                old_i1 = (old_i + 1) % len(delta[old])
                delta[cur].append(delta[old][old_i])
                delta[cur].append([delta[old][old_i][0] + delta[old][old_i1][0], delta[old][old_i][1] + delta[old][old_i1][1]])

        delta = delta[k % 2]
                
        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable_step(i, j, i + d[0], j + d[1]):#self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        return neighbors


    def get_size(self):
        return (self._height, self._width)


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

    def __init__(self, i, j, g = 0, h = 0, F = None, parent = None, k = 0):
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


    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)


    def __lt__(self, other):
        '''
        Comparison between self and other. Returns is self < other (self has higher priority).

        In this lab we limit ourselves to cardinal-only uniform-cost moves (cost = 1) and
        Manhattan distance for A*, so g, h, f-values are integers, so the comparison is straightforward
        '''
        return self.F < other.F or ((self.F == other.F) and (self.h < other.h))\
        or ((self.F == other.F) and (self.h == other.h) and (self.k > other.k))


    def __hash__(self):
        return hash((self.i, self.j))
