from ast_class import AST
from operator_class import Operator
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


def find_top_brackets(asts: List[AST]) -> List[int]:
    """
        Finds the closest brackets of the expression.
        :raises ValueError: If brackets are not balanced.
        :param asts: List of ASTs.
        :return: (start_point, end_point) of the closest brackets.
    """
    top_brackets: List[int] = []
    result_brackets: List[int] = [-1, -1]
    min_length: int = 99999999
    capture_index: int = 0
    for i, ast in enumerate(asts):
        if ast.root.name == "(":
            top_brackets.append(i)
            if asts[i + 1].root.name == '!':
                continue
            ast.root.capture_group = capture_index
            capture_index += 1
        elif ast.root.name == ")":
            if len(top_brackets) == 0:
                raise ValueError("Unbalanced brackets")
            start_point = top_brackets.pop()
            if i - start_point < min_length:
                min_length = i - start_point
                result_brackets = [start_point, i]
    return result_brackets


def bracket_pair_to_ast(asts: List[AST], brackets: List[int]) -> None:
    """
    Converts bracket pairs to ASTs.
    :param asts: List of ASTs.
    :param brackets: Tuple of (start_point, end_point)
    :return: None
    """
    if asts[brackets[0]].root.capture_group is not None:
        capture_group: int = asts[brackets[0]].root.capture_group
        for i in range(brackets[0] + 1, brackets[1]):
            asts[i].root.capture_group = capture_group

    # check for "+", "*" and "{}" operators
    i: int = brackets[0] + 1
    while i < brackets[1]:
        if asts[i].root.left is not None:
            i += 1
            continue
        current_operand = asts[i].root.operand
        if current_operand and current_operand.type == Operator.Type.REPEAT:
            asts[i - 1].ast_left(asts[i].root)
            asts.pop(i - 1)
            brackets[1] -= 1
            i -= 1
        i += 1

    # check for "CONCATENATE" operator
    i = brackets[0] + 2
    while (brackets[1] - brackets[0] != 2) and (i < brackets[1]):
        if (not asts[i].root.check_op(Operator.Type.PREDICTIVE, Operator.Type.ALTER) and
                not asts[i - 1].root.check_op(Operator.Type.PREDICTIVE, Operator.Type.ALTER)):
            capture_group: int = asts[i].root.capture_group
            middle_node: AST.Node = AST.Node("")
            middle_node.capture_group = capture_group
            asts[i - 1].ast_right(middle_node, asts[i].root)
            asts.pop(i)
            brackets[1] -= 1
        else:
            i += 1

    # check for "PREDICTIVE" and "ALTER" operator
    if len(asts) != 1:
        i = brackets[0] + 1
        while i < brackets[1]:
            if asts[i].root.left is not None:
                i += 1
                continue
            if asts[i].root.check_op(Operator.Type.PREDICTIVE, Operator.Type.ALTER):
                asts[i - 1].ast_right(asts[i].root, asts[i + 1].root)
                asts.pop(i + 1)
                asts.pop(i)
                brackets[1] -= 2
                i -= 1
            i += 1


def concat_asts(asts: List[AST]) -> None:
    """
    Concatenates the ASTs.
    :param asts: List of ASTs.
    :return: None
    """
    while len(asts) > 1:
        middle_node: AST.Node = AST.Node("")
        asts[0].ast_right(middle_node, asts[1].root)
        asts.pop(1)


def tokenize(expr: str) -> Tuple[List[AST], int]:
    """
    Tokenizes the expression.
    :param expr: Expression in string type.
    :return: List of ASTs
    """
    asts: List[AST] = []
    start_elements: int = 0
    i: int = 0
    while i < len(expr):
        element = expr[i]
        if element == '(':
            start_elements += 1

        name: str | None = element
        if element == '%':
            asts.append(AST(element + expr[i + 1], non_operand=False))
            i += 2
            continue
        elif element == '{':
            j: int = i + 1
            while expr[j] != '}':
                name += expr[j]
                j += 1
            name += expr[j]
            i = j
        elif element == '[':
            j: int = i + 1
            while expr[j] != ']':
                name += expr[j]
                j += 1
            name += expr[j]
            i = j
        asts.append(AST(name))
        i += 1
    return asts, start_elements


def remove_shielding_symbols(ast: AST) -> None:
    def check_recursive(node: AST.Node) -> None:
        if node.name and node.name[0] == "%":
            node.name = node.name[1:]
        if node.left:
            check_recursive(node.left)
        if node.right:
            check_recursive(node.right)

    check_recursive(ast.root)


def build_ast(expr: str) -> AST:
    """
    Builds the AST.
    :param expr: Expression in string type.
    :return: AST
    """
    logger.info(f"Building AST for {expr}")
    asts, start_elements = tokenize(expr)

    if asts[0].root.name != '(' or asts[-1].root.name != ')':
        asts = [AST(AST.Node('('))] + asts + [AST(AST.Node(')'))]
        start_elements += 1

    while start_elements != 0:
        closest_brackets: List[int] = find_top_brackets(asts)
        bracket_pair_to_ast(asts, closest_brackets)
        while closest_brackets[1] - closest_brackets[0] > 2:
            capture_group: int = asts[closest_brackets[0] + 1].root.capture_group
            middle_node: AST.Node = AST.Node("")
            middle_node.capture_group = capture_group
            asts[closest_brackets[0] + 1].ast_right(middle_node, asts[closest_brackets[1] + 2].root)
            asts.pop(closest_brackets[0] + 2)
            closest_brackets[1] -= 1
        asts.pop(closest_brackets[0])
        asts.pop(closest_brackets[1] - 1)
        start_elements -= 1
    closest_brackets = [0, len(asts) - 1]
    bracket_pair_to_ast(asts, closest_brackets)
    concat_asts(asts)
    remove_shielding_symbols(asts[0])
    logger.info(asts[0].text())
    return asts[0]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    x = build_ast("(ABCD|AB+%))|(AB*){2,3}((SAD)+)")
