import re

number_regex = re.compile(r"[0-5][0-9]{}")

current_regex = re.compile(r"irc://(?P<server_name>[\w]+):([1-6])")