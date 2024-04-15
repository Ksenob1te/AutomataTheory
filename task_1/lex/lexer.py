import ply.lex as lex
import ply.yacc as yacc
from typing import Union, Tuple
import time


# irc://имя_сервера:номер_порта/имя_канала?пароль
tokens = (
    "IRC_PART", "TEXT_PART", "PORT_PART", "SLASH", "PASSWORD"
)


def t_IRC_PART(t):
    r"""irc://"""
    if __name__ == "__main__":
        print("irc")
    return t


def t_TEXT_PART(t):
    r"""\w+"""
    if __name__ == "__main__":
        print("TEXT:", t.value)
    return t


def t_PORT_PART(t):
    r""":(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[0-5][0-9]{4}|[0-9]{1,4})"""
    if __name__ == "__main__":
        print("PORT:", t.value)
    return t


def t_PASSWORD(t):
    r"""\?(\w+)"""
    if __name__ == "__main__":
        print("PASSWORD:", t.value)
    return t


t_SLASH = r"/"
t_ignore = ""


def t_error(t):
    if __name__ == "__main__":
        print("Illegal character '%s' at line' %s'" % (t.value[0] , t.lexer.lineno ))
    t.lexer.skip(1)
    return t


def p_main(p):
    """
    main : IRC_PART TEXT_PART after_server
    """
    p[0] = p[2]


def p_after_server(p):
    """
    after_server : PORT_PART after_port
                 | after_port
    """


def p_after_port(p):
    """
    after_port :
               | SLASH after_slash
    """


def p_after_slash(p):
    """
    after_slash :
                | TEXT_PART PASSWORD
                | PASSWORD
                | TEXT_PART
    """


def p_error(p):
    if __name__ == "__main__":
        print('Unexpected token:', p)
    return


lexer = lex.lex()
parser = yacc.yacc(optimize=1)
if __name__ == "__main__":
    s = "irc://Q/AzoO"
    result_t = parser.parse(s)
    print(result_t)


def resolve(input_str: str) -> Tuple[Union[str, None], float]:
    start_timer = time.time()
    if len(input_str) > 80:
        return None, time.time() - start_timer
    result: Union[str, None] = parser.parse(input_str)
    return result, time.time() - start_timer
