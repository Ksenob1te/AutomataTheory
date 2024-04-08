import random
import string

alnum = string.ascii_letters + string.digits


def get_string() -> str:
    result = "irc://"
    has_port, has_ch_name, has_pass = random.choices([False, True], k=3)
    port = (":" + str(random.randint(1, 65535))) if has_port else ""
    sizes = [random.randint(1, 80),
             len(port),
             random.randint(1, 80) if has_ch_name else 0,
             random.randint(1, 80) if has_pass else 0]

    while sum(sizes) > 72:
        sizes[0] = random.randint(1, 80)
        sizes[2] = random.randint(1, 80)
        sizes[3] = random.randint(1, 80)

    result += "".join(random.choices(alnum, k=sizes[0]))
    result += port
    if not has_ch_name and not has_pass:
        result += random.choice(["/", ""])
        return result
    result += "/"
    result += "".join(random.choices(alnum, k=sizes[2]))
    if has_pass:
        result += "?"
        result += "".join(random.choices(alnum, k=sizes[3]))
    return result



