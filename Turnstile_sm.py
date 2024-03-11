# ex: set ro:
# DO NOT EDIT.
# generated by smc (http://smc.sourceforge.net/)
# from file : Turnstile.sm

import statemap


class TurnstileState(statemap.State):

    def Entry(self, fsm):
        pass

    def Exit(self, fsm):
        pass

    def coin(self, fsm):
        self.Default(fsm)

    def passs(self, fsm):
        self.Default(fsm)

    def Default(self, fsm):
        msg = "\n\tState: %s\n\tTransition: %s" % (
            fsm.getState().getName(), fsm.getTransition())
        raise statemap.TransitionUndefinedException(msg)

class MainMap_Default(TurnstileState):
    pass

class MainMap_Locked(MainMap_Default):

    def coin(self, fsm):
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt.unlock()
        finally:
            fsm.setState(MainMap.Unlocked)
            fsm.getState().Entry(fsm)


    def passs(self, fsm):
        ctxt = fsm.getOwner()
        endState = fsm.getState()
        fsm.clearState()
        try:
            ctxt.alarm()
        finally:
            fsm.setState(endState)


class MainMap_Unlocked(MainMap_Default):

    def coin(self, fsm):
        ctxt = fsm.getOwner()
        endState = fsm.getState()
        fsm.clearState()
        try:
            ctxt.thankyou()
        finally:
            fsm.setState(endState)


    def passs(self, fsm):
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt.lock()
        finally:
            fsm.setState(MainMap.Locked)
            fsm.getState().Entry(fsm)


class MainMap(object):

    Locked = MainMap_Locked('MainMap.Locked', 0)
    Unlocked = MainMap_Unlocked('MainMap.Unlocked', 1)
    Default = MainMap_Default('MainMap.Default', -1)

class Turnstile_sm(statemap.FSMContext):

    def __init__(self, owner):
        statemap.FSMContext.__init__(self, MainMap.Locked)
        self._owner = owner

    def __getattr__(self, attrib):
        def trans_sm(*arglist):
            self._transition = attrib
            getattr(self.getState(), attrib)(self, *arglist)
            self._transition = None
        return trans_sm

    def enterStartState(self):
        self._state.Entry(self)

    def getOwner(self):
        return self._owner

# Local variables:
#  buffer-read-only: t
# End:
