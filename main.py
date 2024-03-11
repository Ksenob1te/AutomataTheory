import Turnstile_sm


class Turnstile:
    def __init__(self):
        self._fsm = Turnstile_sm.Turnstile_sm(self)

    def alarm(self):
        print("Alarming!")

    def thankyou(self):
        print("Thanks!")

    def lock(self):
        print("Locked!")

    def unlock(self):
        print("Unlocked!")


if __name__ == '__main__':
    ts = Turnstile()
    ts._fsm.coin()
    ts._fsm.passs()