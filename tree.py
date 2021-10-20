class Tree:
    def __init__(self, value):
        self.root = Node(value, 0)


class Node:
    def __init__(self, value, level):
        self.value = value
        self.level = level
        self.children = []
