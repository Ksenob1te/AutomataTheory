import random
import string

alnum = string.ascii_letters + string.digits


def get_string(server_name:str = None) -> str:
    result = "irc://"
    has_port, has_ch_name, has_pass = random.choices([False, True], k=3)
    port = (":" + str(random.randint(1, 65535))) if has_port else ""
    sizes = [100,
             len(port),
             random.randint(1, 80) if has_ch_name else 0,
             random.randint(1, 80) if has_pass else 0]

    while sum(sizes) > 72:
        if not server_name:
            sizes[0] = random.randint(1, 80)
        else:
            sizes[0] = len(server_name)
        sizes[2] = random.randint(1, 80)
        sizes[3] = random.randint(1, 80)

    if not server_name:
        result += "".join(random.choices(alnum, k=sizes[0]))
    else:
        result += server_name
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



