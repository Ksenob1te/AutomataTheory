from ..nfa import build_nfa
from .dfa_builder import build_dfa
from ..my_ast import build_ast
from .dfa_minimizer import dfa_minimizer
import logging

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
#                         format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
#     # x = build_ast("(ABCD|AB+%))|(AB*){2,3}((SAD)+)")
#     # x = build_ast("(AD|B+%))|(AB*){0,3}")
#     x = build_ast("(AD|B+%)){1, 3}")
#     # x = build_ast("A*A*A*")
#     # x = build_ast("(a|b)*")
#
#     x = build_nfa(x, 1)
#     logging.info(str(x))
#     x = build_dfa(x)
#     logging.info(str(x))
#     x = dfa_minimizer(x)
#     logging.info(str(x))