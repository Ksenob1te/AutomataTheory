import random
import string
from typing import Tuple
import time
import sys

from regex import resolver_regex
from smc import resolver_smc
from lex import lexer
from gen import correct_generator
from gen import incorrect_generator


# irc://server2:25565/randomname?password
if __name__ == '__main__':
    print(sys.argv)
    random.seed(time.time())

    lex_timer, smc_timer, regex_timer = 0, 0, 0
    server_dict = {}
    incorrect_iter = 0
    selected_s_count = 0

    def check(resolver_type, checker_s: str) -> Tuple[bool, float]:
        global server_dict, incorrect_iter
        result, timer = resolver_type(checker_s)
        # if (result is None and type_s != 0) or (result is not None and type_s == 0):
        #     incorrect_iter += 1
        if result:
            server_dict[result] = server_dict.get(result, 0) + 1
        return bool(result), timer

    for line in open("input.txt"):
        line = line.replace("\n", "")
        print(line)
        if "lex" in sys.argv:
            result, lex_timer = check(lexer.resolve, line)
            print(f"Lex parser: {result} in {lex_timer}")
        if "smc" in sys.argv:
            result, smc_timer = check(resolver_smc.resolve, line)
            print(f"Smc parser: {result} in {smc_timer}")
        if "regex" in sys.argv:
            result, regex_timer = check(resolver_regex.resolve, line)
            print(f"Regex parser: {result} in {smc_timer}")

        # if type_s == 2:
        #     selected_s_count += 1
        # input_file.close()
    print(smc_timer, regex_timer, lex_timer, incorrect_iter)
    # print(server_dict[selected_servername] / 3, selected_s_count)
