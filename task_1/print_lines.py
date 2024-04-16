import random
from typing import Tuple
from gen import incorrect_generator, correct_generator

selected_servername = [
    "SERVER_FIRST",
    "SERVER_SECOND",
    "SERVER_THIRD",
    "SERVER_FOURTH",
    "SERVER_FIFTH",
    "SERVER_SIXTH",
    "SERVER_SEVENTH"
]

def generate_random() -> Tuple[str, int]:
    global selected_servername
    x = random.randint(0, 2)
    s = ""
    if x == 0:
        s = incorrect_generator.get_string()
    elif x == 1:
        s = correct_generator.get_string()
    elif x == 2:
        s = correct_generator.get_string(random.choice(selected_servername))
    return s, x


if __name__ == "__main__":
    file = open("input.txt", "w")
    for i in range(10000):
        file.write(generate_random()[0] + "\n")