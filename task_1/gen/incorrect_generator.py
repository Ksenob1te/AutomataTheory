import random
import string

# irc://имя_сервера:номер_порта/имя_канала?пароль

MAX_PER_PART: int = 80

def get_string() -> str:
    printable = string.printable
    is_good = True
    result = ""
    while is_good:
        has_port, has_ch_name, has_pass = random.choices([False, True], k=3)
        sizes = [random.randint(0, MAX_PER_PART),
                 random.randint(0, MAX_PER_PART) if has_port else 0,
                 random.randint(0, MAX_PER_PART) if has_ch_name else 0,
                 random.randint(0, MAX_PER_PART) if has_pass else 0]

        irc_part = "".join(random.choices(printable, k=6))
        if irc_part != "irc://":
            is_good = False

        server_name = "".join(random.choices(printable, k=sizes[0]))
        if not server_name.isalnum():
            is_good = False

        port = ""
        if has_port:
            port = "".join(random.choices(printable, k=sizes[1]))
            if not port.isnumeric() or (1 > int(port) or int(port) > 65535):
                is_good = False

        ch_name = ""
        if has_ch_name:
            ch_name = "".join(random.choices(printable, k=sizes[2]))
            if not ch_name.isalnum():
                is_good = False

        password = ""
        if has_pass:
            password = "".join(random.choices(printable, k=sizes[3]))
            if not password.isalnum():
                is_good = False

        has_colon, has_slash, has_question = random.choices([False, True], k=3)

        if has_question and not has_pass:
            is_good = False
        if has_colon and not has_port:
            is_good = False

        result = f"{irc_part}{server_name}{':' if has_colon else ''}{port}{'/' if has_slash else ''}{ch_name}{'?' if has_question else ''}{password}"
        if len(result) > 80:
            is_good = False
    return result.replace("\n", "").replace("\r", "")