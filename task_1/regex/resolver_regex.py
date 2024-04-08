import re

number_regex = r"(6553[0-5]|655[0-2][1-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[0-5][0-9]{4}|[0-9]{1,4})"
current_regex = re.compile(r"^irc://(?P<server_name>\w+)(:(?P<port>{0}))?($|/(?P<name>\w+)?(\?(?P<passw>\w+))?$)".format(number_regex))

print(bool(current_regex.match("irc://server2:12312/randomname?qwe")))