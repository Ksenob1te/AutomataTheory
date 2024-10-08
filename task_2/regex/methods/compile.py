from ..classes import *
import logging
logger = logging.getLogger(__name__)

def re_compile(expr: str) -> Automat:
    """
    Compile a regex expression into a DFA with logging
    :param expr: str - regex expression
    :return: Automat - DFA
    """
    expr_ast: AST = build_ast(expr)
    logger.info(f"Built AST for the regex: {expr}\n{expr_ast.text()}")
    expr_nfa: Automat = build_nfa(expr_ast, 1)
    logger.info(f"Built NFA for the regex: {expr}\n{str(expr_nfa)}")
    expr_dfa: Automat = build_dfa(expr_nfa)
    logger.info(f"Built DFA for the regex: {expr}\n{str(expr_dfa)}")
    expr_dfa = dfa_minimizer(expr_dfa)
    expr_dfa.fill_search_capture_map()
    logger.info(f"Minimized DFA for the regex: {expr}\n{str(expr_dfa)}")
    return expr_dfa

