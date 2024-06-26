import re
from typing import Union, Tuple
import time

number_regex = r"(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[0-5][0-9]{4}|[0-9]{1,4})"
current_regex = re.compile(r"^irc://(?P<server_name>\w+)(:(?P<port>{0}))?($|/(?P<name>\w+)?(\?(?P<passw>\w+))?)?$".format(number_regex))



def resolve(input_str: str) -> Tuple[Union[str, None], float]:
    start_timer = time.time()
    if len(input_str) > 80:
        return None, time.time() - start_timer
    result = current_regex.match(input_str)
    if result:
        return result.group("server_name"), time.time() - start_timer
    else:
        return None, time.time() - start_timer


if __name__ == "__main__":
    print(bool(current_regex.match("irc://Ss2On9b0jFp5zyJyDUXxrKhj9l6GBrYy/?BRcWlk1pIgmHMhOJ2jOM5K6sqUNyyIU20V")))
