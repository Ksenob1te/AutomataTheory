import logging

from .classes import *
from .methods import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    x = "(ABCD|AB+%))|(AB*){2,3}((SAD)+)"
    # x = "(AD|B+%))|(AB*){0,3}"
    # x = "(AD|B+%)){1, 3}"
    # x = "(abcde)|(bcdf)"
    # x = "A*A*A*"
    # x = "(a|b)*"

    print(re_findall(x, "123AB)456ABBBBABASADSAD123"))