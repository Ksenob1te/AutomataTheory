from .nfa_builder import build_nfa
from ..my_ast import build_ast
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    # x = build("(ABCD|AB+%))|(AB*){2,3}((SAD)+)")
    # x = build("(AD|B+%))|(AB*){0,3}")
    x = "a|bc"
    ast = build_ast(x)
    nfa = build_nfa(ast, 1)
    nfa2 = build_nfa(ast, 1)
    logging.info(str(nfa2))
