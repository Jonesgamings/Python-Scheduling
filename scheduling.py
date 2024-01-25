class Node:

    def __init__(self, name, parents, children = {}, early_start = None, late_start = None) -> None:
        self.name = name
        self.parents = parents
        self.children = children
        self.early_start = early_start
        self.late_start = late_start
        self.completed_forward = False if early_start == None else True
        self.completed_backward = False if late_start == None else True

        self.generate()

    def generate(self):
        if len(self.parents) != 0:
            for parent, weight in self.parents.items():
                parent.add_child(self, weight)

        elif len(self.children) != 0:
            for child, weight in self.children.items():
                child.add_parent(self, weight)

    def add_parent(self, parent, weight):
        if parent in self.parents.values(): return
        self.parents[parent] = weight

    def add_child(self, child, weight):
        if child in self.children.values(): return
        self.children[child] = weight

    def forward_pass(self):
        if len(self.parents) == 0:
            self.early_start = 0
            return

        max_w = None
        for parent, weight in self.parents.items():
            if not self.completed_forward: parent.forward_pass()

            if max_w == None: max_w = parent.early_start + weight
            elif weight + parent.early_start > max_w: max_w = weight + parent.early_start

        self.early_start = max_w

    def copy(self):
        return Node(self.name, self.parents, self.children)

    def backward_pass(self):
        if len(self.children) == 0:
            self.late_start = self.early_start
            return

        min_w = None
        for child, weight in self.children.items():
            if not self.completed_backward: child.backward_pass()

            if min_w == None: min_w = child.late_start - weight
            elif child.late_start - weight < min_w:  min_w = child.late_start - weight

        self.late_start = min_w

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Node): 
            return False
        
        if __value.name != self.name:
            return False
        
        return True

if __name__ == "__main__":
    pass