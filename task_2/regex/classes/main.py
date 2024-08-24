from automat.automat_class import *

if __name__ == "__main__":
    fill_transition_sieve()
    aut = Automat(1, "a")
    op = Operator("{2, 3}")
    aut._repeat_automat(op)
    x = 1


