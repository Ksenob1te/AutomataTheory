from __future__ import annotations
from .operator_class import Operator
from treelib import Tree
from typing import List


class AST(object):
    """
    Abstract Syntax Tree class.
    """
    class Node:
        """
        Node class for AST.
        """
        name: str = None
        operand: Operator = None
        capture_group: List[int] = None
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
            if self.name or not self.operand:
                return self.name + f" ({self.capture_group})"
            else:
                return self.operand.type.name + f" ({self.capture_group})"

    root: AST.Node = None

    def __init__(self, root: AST.Node | str, non_operand: bool = False):
        if type(root) is str:
            self.root = AST.Node(root, non_operand)
        elif type(root) is AST.Node:
            self.root = root

    def __str__(self):
        return str(self.root)

    def text(self) -> str:
        """
        Returns the text representation of the AST with tree view
        :return: str
        """
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
        """
        Moves current root to the left of the new root.
        :param new_root:
        :return:
        """
        new_root.left = self.root
        self.root = new_root

    def ast_right(self, new_root: Node, right: AST.Node):
        """
        Moves current root to the left of the new root and sets the right node.
        :param new_root: Node to be set as a new root.
        :param right: AST Node to be set as a right node.
        :return:
        """
        new_root.left = self.root
        new_root.right = right
        self.root = new_root

    def set_left(self, left: Node):
        """
        Sets the left node of the current root.
        :param left:
        :return:
        """
        self.root.left = left

    def set_right(self, right: Node):
        """
        Sets the right node of the current root.
        :param right:
        :return:
        """
        self.root.right = right


