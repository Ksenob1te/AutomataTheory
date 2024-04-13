import ply.lex as lex


# irc://имя_сервера:номер_порта/имя_канала?пароль
tokens = (
    "IRC_PART", "SERVER_PART", "PORT_PART", "SLASH_PART", "CHANNEL_NAME", "PASSWORD"
)


def t_IRC_PART(t):
    r"""irc://"""
