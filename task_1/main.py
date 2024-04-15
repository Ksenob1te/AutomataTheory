import random
from typing import Tuple
import time

from regex import resolver_regex
from smc import resolver_smc
from lex import lexer
from gen import correct_generator
from gen import incorrect_generator


# irc://server2:25565/randomname?password
if __name__ == '__main__':

    selected_servername = "TESTING"
    def generate_random() -> Tuple[str, int]:
        x = random.randint(0, 2)
        s = ""
        if x == 0:
            s = incorrect_generator.get_string()
        elif x == 1:
            s = correct_generator.get_string()
        elif x == 2:
            s = correct_generator.get_string(selected_servername)
        return s, x

    # ts = resolver_smc.Resolver("irc://bMmFDVj798kQDheffp139xRX/WPNLYdqMkSLW")
    # ts.run()

    lex_timer, smc_timer, regex_timer = 0, 0, 0
    server_dict = {}
    incorrect_iter = 0
    selected_s_count = 0

    for i in range(1, 100000):
        checker_s, type_s = generate_random()
        # print(s, end=": ")

        def check(resolver_type):
            global server_dict, incorrect_iter, checker_s
            result, timer = resolver_type(checker_s)
            if (result is None and type_s != 0) or (result is not None and type_s == 0):
                incorrect_iter += 1
            if result:
                server_dict[result] = server_dict.get(result, 0) + 1
            return timer

        lex_timer += check(lexer.resolve)
        smc_timer += check(resolver_smc.resolve)
        regex_timer += check(resolver_regex.resolve)

        if type_s == 2:
            selected_s_count += 1
        # check = True
        # if not resolver_smc.resolve(s):
        #     print("SMC", end=" ")
        #     check = False
        # if not lexer.resolve(s):
        #     print("LEXER", end=" ")
        #     check = False
        # if not resolver_regex.resolve(s):
        #     print("REGEX", end=" ")
        #     check = False
        # if not check:
        #     print(s)
    print(smc_timer, regex_timer, lex_timer, incorrect_iter)
    print(server_dict[selected_servername] / 3, selected_s_count)
