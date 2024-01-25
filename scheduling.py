class Node:

    def __init__(self, name, parents, children = {}, early_start = None, late_start = None) -> None:
        self.name = name
        self.parents = parents.copy()
        self.children = children.copy()
        self.early_start = early_start
        self.late_start = late_start
        self.completed_forward = False if early_start == None else True
        self.completed_backward = False if late_start == None else True

        self.arcs = []

        self.generate()
        self.generate_arcs()

    def generate_arcs(self):
        for parent, weight in self.parents.items():
            arc = Arc(parent, self, weight)
            self.arcs.append(arc)

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
            if not parent.completed_forward: parent.forward_pass()

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
            if not child.completed_backward: child.backward_pass()

            if min_w == None: min_w = child.late_start - weight
            elif child.late_start - weight < min_w:  min_w = child.late_start - weight

        self.late_start = min_w

    def __hash__(self) -> int:
        return hash(self.name) * 32

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Node): 
            return False
        
        if __value.name != self.name:
            return False
        
        return True

    def __repr__(self) -> str:
        return f"{self.name}: ({self.early_start}, {self.late_start})"

    def __str__(self) -> str:
        return f"{self.name}: ({self.early_start}, {self.late_start})"

class Arc:

    def __init__(self, start_node, end_node, weight) -> None:
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.name = f"{self.start_node.name}->{self.end_node.name}"
        self.total_float = None
        self.independent_float = None
        self.interfering_float = None

    def calculate_float(self):
        self.total_float = (self.end_node.late_start - self.start_node.early_start) - self.weight
        self.independent_float = max((self.end_node.early_start - self.start_node.late_start) - self.weight, 0)
        self.interfering_float = self.total_float - self.independent_float

    def __repr__(self) -> str:
        return f"{self.name}: ({self.total_float}, {self.independent_float}, {self.interfering_float})"

    def __str__(self) -> str:
        return f"{self.name}: ({self.total_float}, {self.independent_float}, {self.interfering_float})"

def do_passes(nodes):
    nodes[-1].forward_pass()
    nodes[0].backward_pass()

def get_arcs(nodes):
    ARCS = []
    for node in nodes:
        ARCS += node.arc

    return ARCS

def calculate_floats(arcs):
    for arc in ARCS:
        arc.calculate_float()

def get_critical_path(arcs):
    CRITICAL = []
    for arc in arcs:
        if arc.total_float == 0:
            CRITICAL.append(arc)

    return CRITICAL

if __name__ == "__main__":
    A = Node("A", {})
    B = Node("B", {A:7})
    C = Node("C", {A:2, B:0})
    D = Node("D", {B:6, C:0})
    E = Node("E", {C:3, D:0})
    F = Node("F", {D:9, E:11})
    NODES = [A, B, C, D, E, F]
    ARCS = []
    for node in NODES:
        ARCS += node.arcs

    F.forward_pass()
    A.backward_pass()

    for arc in ARCS:
        arc.calculate_float()

    print(NODES)
    print(ARCS)
    print(get_critical_path(ARCS))
