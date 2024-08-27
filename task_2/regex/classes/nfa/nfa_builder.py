import logging

from ..my_ast import AST, Operator
from ..automat import Automat, fill_transition_sieve

def build_nfa(ast: AST, automat_id: int) -> Automat:
    fill_transition_sieve()
    if ast.root.left is None and ast.root.right is None:
        if ast.root.check_op(Operator.Type.SET_RANGE):
            atm: Automat = Automat(automat_id=automat_id, operator=ast.root.operand)
        else:
            atm: Automat = Automat(automat_id=automat_id, transition=ast.root.name)
        for group in ast.root.capture_group:
            atm.add_capture_all_states(group)
        return atm

    nfa_left: Automat | None = None
    nfa_right: Automat | None = None

    if ast.root.left is not None:
        ast_left: AST = AST(ast.root.left)
        nfa_left = build_nfa(ast_left, automat_id + 1)
        # logging.info(str(nfa_left))
    if ast.root.right is not None:
        ast_right: AST = AST(ast.root.right)
        id_right = (nfa_left.id + 1) if (type(nfa_left) != type(None)) else automat_id + 1
        nfa_right = build_nfa(ast_right, id_right)
        # logging.info(str(nfa_right))

    if ast.root.left is None or ast.root.right is None:
        selected_nfa: Automat = nfa_left if nfa_left is not None else nfa_right
        if ast.root.check_op(Operator.Type.REPEAT):
            selected_nfa.repeat_automat(ast.root.operand)
            for group in ast.root.capture_group:
                selected_nfa.add_capture_all_states(group)
            return selected_nfa
        else:
            logging.error("Incorrect AST while trying to build NFA")
            raise ValueError("Incorrect AST while trying to build NFA")
    else:
        if ast.root.check_op(Operator.Type.CONCAT):
            nfa_left.cat_automat(nfa_right)
        elif ast.root.check_op(Operator.Type.ALTER):
            nfa_left.alter_automat(nfa_right)
        else:
            logging.error("Incorrect AST while trying to build NFA")
            raise ValueError("Incorrect AST while trying to build NFA")
        for group in ast.root.capture_group:
            nfa_left.add_capture_all_states(group)
        return nfa_left



