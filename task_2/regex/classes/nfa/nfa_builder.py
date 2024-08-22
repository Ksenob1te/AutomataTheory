from ..ast import AST
from ..automat import Automat

def build_nfa(ast: AST, re_id: int) -> Automat:
    if ast.root.left is None and ast.root.right is None:


