from sortedcontainers import SortedList as sorted_list
from .structures import Node, AnyaNode


class Open:

    def __init__(self):
        self.elements = sorted_list()
        self.dict = dict()

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def is_empty(self):
        if len(self.elements) != 0:
            return False
        return True

    def add_node(self, item, *args):
        try:
            in_dict = self.dict[(item.i, item.j)]
            if in_dict.F > item.F:
                self.elements.remove(in_dict)
                self.elements.add(item)
                self.dict.update([((item.i, item.j), item)])
        except KeyError:
            self.dict.update([((item.i, item.j), item)])
            self.elements.add(item)

    def get_best_node(self, *args):
        return self.elements.pop(0)


class Closed:

    def __init__(self):
        self.elements = set()
        self.indexes = set()

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def add_node(self, item : Node):
        self.elements.add(item)
        self.indexes.add((item.i, item.j, item.is_left))

    def was_expanded(self, i, j, is_left):
        return (i, j, is_left) in self.indexes


class OpenAnya:

    def __init__(self):
        self.elements = sorted_list()

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def is_empty(self):
        if len(self.elements) != 0:
            return False
        return True

    def add_node(self, item: AnyaNode, *args):
        try:
            self.elements.add(item)
        except KeyError:
            self.elements.add(item)

    def get_best_node(self, *args):
        return self.elements.pop(0)
