from task_1.smc import Resolver_sm


class Element:
    element: str = ''

    def __init__(self, element: str = ''):
        self.element = element

    def is_number(self) -> bool:
        return self.element.isnumeric()

    def is_letter(self) -> bool:
        return self.element.isalpha()

    def is_alnum(self) -> bool:
        return self.element.isalnum()

    def is_irc(self) -> bool:
        return self.element == "irc://"

    def __get__(self) -> str:
        return self.element


class Resolver:
    current_context: int = None
    current_id: int = 0

    check_string: str = None
    server_name: str = None
    port: int = None
    channel_name: str = None
    password: str = None

    def __init__(self, string: str):
        self.check_string = string
        self.current_id = 0
        self.current_state = 0
        self._fsm = Resolver_sm.Resolver_sm(self)

    def skip(self, amount: int = 1) -> None:
        self.current_id += amount

    def get(self, amount: int = 1) -> Element:
        return Element(self.check_string[self.current_id:(self.current_id + amount)])

    def context(self, set_context: int) -> None:
        if set_context == 1:
            self.server_name += self.check_string[self.current_id]
        if set_context == 3:
            self.channel_name += self.check_string[self.current_id]
        if set_context == 4:
            self.password += self.check_string[self.current_id]

    def update_port(self, number: int) -> bool:
        self.port *= 10
        self.port += number
        return 1 <= self.port <= 65535



if __name__ == '__main__':
    ts = Turnstile()
    ts._fsm.coin()
    ts._fsm.passs()