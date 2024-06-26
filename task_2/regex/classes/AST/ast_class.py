from __future__ import annotations
from operator_class import Operator
from treelib import Tree

class AST(object):
    class Node:
        name: str = None
        operand: Operator = None
        capture_group: int = None
        left: AST.Node = None
        right: AST.Node = None

        def check_op(self, *args) -> bool:
            if not self.operand:
                return False
            for arg in args:
                if self.operand.type == arg:
                    return True
            return False


        def __init__(self, name: str = None, non_operand: bool = False):
            if non_operand:
                self.name = name
                return
            else:
                operand = Operator(name)
                if operand is not None:
                    self.operand = operand
                else:
                    self.name = name

        def __str__(self):
            if self.name:
                return self.name
            else:
                return self.operand.type.name


    root: AST.Node = None

    def __init__(self, root: AST.Node | str, non_operand: bool = False):
        if type(root) is str:
            self.root = AST.Node(root, non_operand)
        elif type(root) is AST.Node:
            self.root = root

    def __str__(self):
        return str(self.root)

    def text(self) -> str:
        tree = Tree()

        def add_children(local_root: AST.Node, identifier: int):
            if local_root.left is not None:
                tree.create_node(str(local_root.left), identifier * 2, parent=identifier)
                add_children(local_root.left, identifier * 2)
            if local_root.right is not None:
                tree.create_node(str(local_root.right), identifier * 2 + 1, parent=identifier)
                add_children(local_root.right, identifier * 2 + 1)

        tree.create_node(str(self.root), 1)
        add_children(self.root, 1)
        return f"\n{'-' * 50}\n{tree.show(stdout=False)}{'-' * 50}\n"

    def ast_left(self, new_root: Node):
        new_root.left = self.root
        self.root = new_root

    def ast_right(self, new_root: Node, right: AST.Node):
        new_root.left = self.root
        new_root.right = right
        self.root = new_root

    def set_left(self, left: Node):
        self.root.left = left

    def set_right(self, right: Node):
        self.root.right = right


