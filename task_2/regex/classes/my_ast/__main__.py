import logging
from .ast_builder import build_ast


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    x = build_ast("(ABCD|AB+%))|(AB*){2,3}((SAD)+)[1-3abc]")
    x = build_ast("A|BC")