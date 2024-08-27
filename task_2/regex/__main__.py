import logging

from .classes import *
from .methods import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="ast_logger.log",
                        format=f"%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    x = "(ABCD|CF+%))|(AB*){2,3}((SAD)+)"
    # x = "A{0,1}((SAD)+123)"
    # x = "(!(!AS|S)AD(!SAD|$)*123)"
    # x = "(AD|B+%))|(AB*){0,3}"
    # x = "(AD|B+%)){1, 3}"
    # x = "(abc)|(be)"
    # x = "(B+)"
    # x = "(a|b)*"
    # print(*re_findall(x, "123CF)456ABBBBABABSADSAD1234"))
    # x_1 = "B+A"
    # x_2 = "B*"
    atm = inverse_re(x)
    atm = inverse_re(atm)
    # print(atm)
    print(*re_findall(x, "123CF)456ABBBBABABSADSAD1234"))
    # print(difference_dfa(re_compile(x_1), re_compile(x_2)))
    # atm: Automat = re_compile(x)
    # print(re_k_path(atm))