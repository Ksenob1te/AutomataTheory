from .ast_class import AST
from .operator_class import Operator
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


def set_capture_groups(asts: List[AST]) -> None:
    current_capture: List[int] = []
    max_group = 0
    no_capture_group = False
    for i, ast in enumerate(asts):
        if ast.root.name == "(":
            if asts[i + 1].root.name == '!':
                no_capture_group = True
                continue
            max_group += 1
            current_capture.append(max_group)
        elif ast.root.name == ")":
            if no_capture_group:
                continue
            else:
                no_capture_group = False
            current_capture.pop()
        ast.root.capture_group = current_capture.copy()


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
    for i, ast in enumerate(asts):
        if ast.root.name == "(":
            top_brackets.append(i)
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
    def _bracket_repeat_ast(_asts: List[AST], _brackets: List[int]) -> None:
        i: int = _brackets[0] + 1
        while i < _brackets[1]:
            if _asts[i].root.left is not None:
                i += 1
                continue
            current_operand = _asts[i].root.operand
            if current_operand and current_operand.type == Operator.Type.REPEAT:
                _asts[i - 1].ast_left(_asts[i].root)
                _asts.pop(i - 1)
                _brackets[1] -= 1
                i -= 1
            i += 1

    def _bracket_concat_ast(_asts: List[AST], _brackets: List[int]) -> None:
        i = _brackets[0] + 2
        while (_brackets[1] - _brackets[0] != 2) and (i < _brackets[1]):
            if (not _asts[i].root.check_op(Operator.Type.PREDICTIVE, Operator.Type.ALTER) and
                    not _asts[i - 1].root.check_op(Operator.Type.PREDICTIVE, Operator.Type.ALTER)):
                capture_group: List[int] = _asts[i].root.capture_group
                middle_node: AST.Node = AST.Node("")
                middle_node.capture_group = capture_group
                _asts[i - 1].ast_right(middle_node, _asts[i].root)
                _asts.pop(i)
                _brackets[1] -= 1
            else:
                i += 1

    def _bracket_alt_pred_ast(_ast: List[AST], _brackets: List[int]) -> None:
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

    def _collapse_asts(_asts: List[AST], _from_index: int, _to_index: int) -> None:
        """
        Concatenates the ASTs.
        Resulting ASTs will be on `from_index` index
        :param _asts: List of ASTs.
        :param _from_index: index from where u want to collapse ASTs
        :param _to_index: index from where u want to end collapsing ASTs
        :return: None
        """

        while _to_index - _from_index > 0:
            capture_group: List[int] = _asts[_from_index].root.capture_group
            middle_node: AST.Node = AST.Node("")
            middle_node.capture_group = capture_group
            _asts[_from_index].ast_right(middle_node, _asts[_from_index + 1].root)
            _asts.pop(_from_index + 1)
            _to_index -= 1

    # check for "+", "*" and "{}" operators
    # max priority
    _bracket_repeat_ast(asts, brackets)

    # check for "CONCATENATE" operator
    # second priority
    _bracket_concat_ast(asts, brackets)

    # check for "PREDICTIVE" and "ALTER" operator
    # the lowest priority
    _bracket_alt_pred_ast(asts, brackets)

    # collapse all ASTs after all operations inside a bracket
    _collapse_asts(asts, brackets[0] + 1, brackets[1] - 1)


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
    set_capture_groups(asts)

    if asts[0].root.name != '(' or asts[-1].root.name != ')':
        asts = [AST(AST.Node('('))] + asts + [AST(AST.Node(')'))]
        start_elements += 1

    while start_elements != 0:
        closest_brackets: List[int] = find_top_brackets(asts)
        bracket_pair_to_ast(asts, closest_brackets)
        asts.pop(closest_brackets[1])
        asts.pop(closest_brackets[0])
        start_elements -= 1
    closest_brackets = [-1, len(asts)]
    bracket_pair_to_ast(asts, closest_brackets)
    remove_shielding_symbols(asts[0])
    logger.info(asts[0].text())
    return asts[0]

