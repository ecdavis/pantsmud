import json
import uuid
from pantsmud.driver import auxiliary, hook
from pantsmud.util import error


_sessions = {}


class Session(object):
    def __init__(self, stream):
        self.uuid = uuid.uuid4()
        self.stream = stream
        self.environment = None
        self.identity_uuid = None
        self.mobile_uuid = None
        self.is_client = True
        self.input_handlers = []
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_BRAIN)

    @property
    def identity(self):
        if self.identity_uuid:
            return self.environment.identities[self.identity_uuid]
        else:
            return self.identity_uuid

    @identity.setter
    def identity(self, identity):
        if identity:
            self.identity_uuid = identity.uuid
        else:
            self.identity_uuid = None

    @property
    def mobile(self):
        if self.mobile_uuid:
            return self.environment.mobiles[self.mobile_uuid]
        else:
            return None

    @mobile.setter
    def mobile(self, mobile):
        if mobile:
            self.mobile_uuid = mobile.uuid
        else:
            self.mobile_uuid = None

    @property
    def input_handler(self):
        if len(self.input_handlers) == 0:
            raise error.BrainMissingInputHandlers("Session '%s' has no input handlers." % (str(self.uuid)))
        return self.input_handlers[-1][0]

    @property
    def state(self):
        if len(self.input_handlers) == 0:
            raise error.BrainMissingInputHandlers("Session '%s' has no input handlers." % (str(self.uuid)))
        return self.input_handlers[-1][1]

    def replace_input_handler(self, func, state):
        self.pop_input_handler()
        self.push_input_handler(func, state)

    def push_input_handler(self, func, state):
        self.input_handlers.append((func, state))

    def pop_input_handler(self):
        if len(self.input_handlers) == 0:
            raise error.BrainMissingInputHandlers("Session '%s' has no input handlers." % (str(self.uuid)))
        return self.input_handlers.pop()

    def message(self, name, data=None):
        msg = json.dumps({"message": name, "data": data})
        self.write_line(msg)

    def write(self, msg):
        self.stream.write(msg)

    def write_line(self, msg):
        self.write(msg + "\r\n")

    def close(self):
        self.stream.close()


def open_session(stream):
    s = Session(stream)
    _sessions[stream] = s
    hook.run(hook.HOOK_OPEN_BRAIN, s)
    return s


def close_session(stream):
    s = _sessions[stream]
    hook.run(hook.HOOK_CLOSE_BRAIN, s)
    del _sessions[stream]
    return s


def get_session(stream):
    return _sessions[stream]


def init():
    global _sessions
    _sessions = {}
