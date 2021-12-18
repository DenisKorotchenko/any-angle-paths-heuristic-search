from sortedcontainers import SortedList as sorted_list
from .structures import Node

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

    def add_node(self, item : Node, *args):
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


    def __iter__(self):
        return iter(self.elements)
    

    def __len__(self):
        return len(self.elements)


    def add_node(self, item : Node):
        self.elements.add(item)


    def was_expanded(self, item : Node):
        return item in self.elements


class OpenAndClosed:
    def __init__(self):
        self.elements = sorted_list()
        self.expanded_dict = dict()
        self.reexpanded_dict = dict()
        self.number_of_reexpansions_counter = 0
    
    def __iter__(self):
        return iter(self.elements)
    
    def __len__(self):
        return len(self.elements)

    def is_empty(self):
        return self.__len__() == 0

    def add_node(self, item):
        if (item.i, item.j) in self.expanded_dict:
            if self.expanded_dict[(item.i, item.j)].g > item.g:
                self.expanded_dict.pop((item.i, item.j))
                self.number_of_reexpansions_counter += 1
                self.reexpanded_dict[(item.i, item.j)] = item
            else:
                return False
        self.elements.add(item)
        return True

    def get_best_node(self):
        best_node = self.elements.pop(0)
        while (best_node.i, best_node.j) in self.expanded_dict:
            best_node = self.elements.pop(0)
        self.expanded_dict[(best_node.i, best_node.j)] = best_node
        return best_node

    @property
    def expanded(self):
        return self.expanded_dict.values()

    @property
    def reexpanded(self):
        return self.reexpanded_dict.values()

    @property
    def number_of_reexpansions(self):
        return self.number_of_reexpansions_counter

