import logging
import json
import uuid

from pantsmud import auxiliary, error, hook

_sessions = {}


class Session(object):
    def __init__(self, stream):
        self.uuid = uuid.uuid4()
        self.stream = stream
        self.world = None
        self.mobile_uuid = None
        self.is_user = True
        self.input_handlers = []
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_BRAIN)

    @property
    def mobile(self):
        if self.mobile_uuid is None:
            return None
        else:
            return self.world.mobiles[self.mobile_uuid]

    @mobile.setter
    def mobile(self, val):
        if val is None:
            self.mobile_uuid = None
        else:
            self.mobile_uuid = val.uuid

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

    def push_input_handler(self, func, state):
        self.input_handlers.append((func, state))

    def pop_input_handler(self):
        if len(self.input_handlers) == 0:
            raise error.BrainMissingInputHandlers("Session '%s' has no input handlers." % (str(self.uuid)))
        return self.input_handlers.pop()

    def message(self, name, data=None):
        if data:
            msg = "%s %s" % (name, json.dumps(data))
        else:
            msg = name
        self.write_line(msg)

    def write(self, msg):
        self.stream.write(msg)

    def write_line(self, msg):
        self.write(msg + "\r\n")

    def close(self):
        self.stream.close()


def open_session(stream):
    logging.debug("open_session")
    s = Session(stream)
    _sessions[stream] = s
    hook.run(hook.HOOK_OPEN_BRAIN, s)


def close_session(stream):
    logging.debug("close_session")
    s = _sessions[stream]
    hook.run(hook.HOOK_CLOSE_BRAIN, s)
    del _sessions[stream]


def get_session(stream):
    return _sessions[stream]
