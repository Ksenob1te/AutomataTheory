import re
#
x = re.compile(r"[1-2%123]")

stri = "-%341"
print(x.search(stri).group(0))
# print(type(None) == None)