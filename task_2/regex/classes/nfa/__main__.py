from .nfa_builder import build_nfa
from ..my_ast import build
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    # x = build("(ABCD|AB+%))|(AB*){2,3}((SAD)+)")
    x = build("(AD|B+%))|(AB*){0,3}")
    # x = build("(ABCD|AB+%))|(AB*){2,3}((SAD)+)[1-3abc]")
    x = build_nfa(x, 1)
    logging.info(str(x))
