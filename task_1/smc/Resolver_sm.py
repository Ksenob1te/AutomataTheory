# ex: set ro:
# DO NOT EDIT.
# generated by smc (http://smc.sourceforge.net/)
# from file : Resolver.sm

import statemap


class ResolverState(statemap.State):

    def Entry(self, fsm):
        pass

    def Exit(self, fsm):
        pass

    def next(self, fsm):
        self.Default(fsm)

    def Default(self, fsm):
        msg = "\n\tState: %s\n\tTransition: %s" % (
            fsm.getState().getName(), fsm.getTransition())
        raise statemap.TransitionUndefinedException(msg)

class MainMap_Default(ResolverState):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt.finish(False)
        finally:
            fsm.setState(MainMap.no_match)
            fsm.getState().Entry(fsm)


class MainMap_irc_identify(MainMap_Default):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        if  ctxt.get(6).is_irc() and ctxt.validate()  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.skip(6)
            finally:
                fsm.setState(MainMap.server_name_iden)
                fsm.getState().Entry(fsm)
        else:
            MainMap_Default.next(self, fsm)
        
class MainMap_server_name_iden(MainMap_Default):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        if  ctxt.get().is_alnum()  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.context(1)
                ctxt.skip()
            finally:
                fsm.setState(MainMap.server_name_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.get() == ":" and ctxt.context() == 1 :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.skip()
            finally:
                fsm.setState(MainMap.port_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.get() == "/" and ctxt.context() == 1 :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.skip()
            finally:
                fsm.setState(MainMap.channel_name_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.context() == 1  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.finish(True)
            finally:
                fsm.setState(MainMap.match)
                fsm.getState().Entry(fsm)
        else:
            MainMap_Default.next(self, fsm)
        
class MainMap_port_iden(MainMap_Default):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        if  ctxt.update_port()  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.context(2)
                ctxt.skip()
            finally:
                fsm.setState(MainMap.port_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.get() == "/" and ctxt.context() == 2 :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.skip()
            finally:
                fsm.setState(MainMap.channel_name_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.context() == 2  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.finish(True)
            finally:
                fsm.setState(MainMap.match)
                fsm.getState().Entry(fsm)
        else:
            MainMap_Default.next(self, fsm)
        
class MainMap_channel_name_iden(MainMap_Default):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        if  ctxt.get().is_alnum()  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.context(3)
                ctxt.skip()
            finally:
                fsm.setState(MainMap.channel_name_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.get() == "?" :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.skip()
            finally:
                fsm.setState(MainMap.password_iden)
                fsm.getState().Entry(fsm)
        else:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.finish(True)
            finally:
                fsm.setState(MainMap.match)
                fsm.getState().Entry(fsm)


class MainMap_password_iden(MainMap_Default):

    def next(self, fsm):
        ctxt = fsm.getOwner()
        if  ctxt.get().is_alnum()  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.context(4)
                ctxt.skip()
            finally:
                fsm.setState(MainMap.password_iden)
                fsm.getState().Entry(fsm)
        elif  ctxt.context() == 4  :
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.finish(True)
            finally:
                fsm.setState(MainMap.match)
                fsm.getState().Entry(fsm)
        else:
            MainMap_Default.next(self, fsm)
        
class MainMap_match(MainMap_Default):
    pass

class MainMap_no_match(MainMap_Default):
    pass

class MainMap(object):

    irc_identify = MainMap_irc_identify('MainMap.irc_identify', 0)
    server_name_iden = MainMap_server_name_iden('MainMap.server_name_iden', 1)
    port_iden = MainMap_port_iden('MainMap.port_iden', 2)
    channel_name_iden = MainMap_channel_name_iden('MainMap.channel_name_iden', 3)
    password_iden = MainMap_password_iden('MainMap.password_iden', 4)
    match = MainMap_match('MainMap.match', 5)
    no_match = MainMap_no_match('MainMap.no_match', 6)
    Default = MainMap_Default('MainMap.Default', -1)

class Resolver_sm(statemap.FSMContext):

    def __init__(self, owner):
        statemap.FSMContext.__init__(self, MainMap.irc_identify)
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
