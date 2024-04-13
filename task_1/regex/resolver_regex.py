import re
from typing import Union

number_regex = r"(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[0-5][0-9]{4}|[0-9]{1,4})"
current_regex = re.compile(r"^irc://(?P<server_name>\w+)(:(?P<port>{0}))?($|/(?P<name>\w+)?(\?(?P<passw>\w+))?)?$".format(number_regex))

def resolve(input_str: str) -> Union[str, None]:
    if len(input_str) > 80:
        return None
    result = current_regex.match(input_str)
    if result:
        return result.group("server_name")
    else:
        return None

if __name__ == "__main__":
    print(bool(current_regex.match("irc://Ss2On9b0jFp5zyJyDUXxrKhj9l6GBrYy/?BRcWlk1pIgmHMhOJ2jOM5K6sqUNyyIU20V")))
