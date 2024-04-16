from task_1.smc import Resolver_sm
from typing import Union, Tuple
import time


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

    def __eq__(self, other):
        return self.element == other

    def __str__(self):
        return self.element


class Resolver:
    current_context: int = None
    current_id: int = 0

    check_string: str = None
    server_name: str = ""
    port: int = 0
    channel_name: str = ""
    password: str = ""

    finish_checker: bool = False
    state: bool = False

    def __init__(self, string: str):
        self.check_string = string
        self.current_id = 0
        self.current_state = 0
        self._fsm = Resolver_sm.Resolver_sm(self)

    def run(self):
        while not self.finish_checker:
            self._fsm.next()
        if self.state:
            # print("IT IS CORRECT")
            # print(self.server_name)
            # if self.port:
            #     print(self.port)
            # print(self.channel_name)
            # print(self.password)
            return 1
        else:
            # print("IT IS INCORRECT")
            return 0

    def validate(self):
        return len(self.check_string) <= 80

    def skip(self, amount: int = 1) -> None:
        self.current_id += amount

    def get(self, amount: int = 1) -> Element:
        if self.current_id + amount <= len(self.check_string):
            return Element(self.check_string[self.current_id:(self.current_id + amount)])
        return Element()

    def context(self, set_context: int = None) -> int:
        if set_context is None:
            return self.current_context
        else:
            if self.current_id >= len(self.check_string):
                return -1
        self.current_context = set_context
        element: str = self.check_string[self.current_id]
        if set_context == 1:
            self.server_name += element
        if set_context == 3:
            self.channel_name += element
        if set_context == 4:
            self.password += element
        return self.current_context

    def update_port(self) -> bool:
        if self.current_id >= len(self.check_string):
            return False
        element: str = self.check_string[self.current_id]
        if not element.isnumeric():
            return False
        self.port *= 10
        self.port += int(element)
        return 1 <= self.port <= 65535

    def finish(self, success: bool = False):
        if success:
            self.state = True
        else:
            self.state = False
        self.finish_checker = True


def resolve(input_str: str) -> Tuple[Union[str, None], float]:
    ts = Resolver(input_str)
    start_timer = time.time()
    if ts.run():
        return ts.server_name, time.time() - start_timer
    else:
        return None, time.time() - start_timer


if __name__ == "__main__":
    ts = Resolver("irc://hello:13197/2Kly?STpvA")
    ts.run()
    print(ts.server_name)



