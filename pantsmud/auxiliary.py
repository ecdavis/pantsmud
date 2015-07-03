import logging

log = logging.getLogger(__name__)

AUX_TYPE_ACCOUNT = "account"
AUX_TYPE_LINK = "exit"
AUX_TYPE_PLAYER = "player"
AUX_TYPE_ROOM = "room"
AUX_TYPE_SESSION = "session"
AUX_TYPE_WORLD = "world"
AUX_TYPE_ZONE = "zone"

# aux_type: {name: cls}
_auxiliary_classes = {
    AUX_TYPE_ACCOUNT: {},
    AUX_TYPE_LINK: {},
    AUX_TYPE_PLAYER: {},
    AUX_TYPE_ROOM: {},
    AUX_TYPE_SESSION: {},
    AUX_TYPE_WORLD: {},
    AUX_TYPE_ZONE: {}
}


def install(aux_type, name, cls):
    if aux_type not in _auxiliary_classes:
        log.debug("Adding new auxiliary type: '%s'", aux_type)
        _auxiliary_classes[aux_type] = {}
    if name in _auxiliary_classes[aux_type]:
        raise Exception("TODO")  # TODO
    log.debug("Adding new auxiliary: '%s', class '%s', type '%s'", name, cls.__name__, aux_type)
    _auxiliary_classes[aux_type][name] = cls


def new_data(aux_type):
    assert aux_type in _auxiliary_classes
    data = {}
    if aux_type not in _auxiliary_classes:
        return data
    for name, cls in _auxiliary_classes[aux_type].itervalues():
        data[name] = cls()
    return data


def load_data(aux, data):
    aux_keys = set(aux.keys())
    data_keys = set(data.keys())
    keys = aux_keys.union(data_keys)
    if __debug__:
        if len(aux_keys.difference(keys)) > 0:
            for key in aux_keys.difference(keys):
                log.debug("could not find stored data for auxiliary key '%s'", key)
        if len(data_keys.difference(keys)) > 0:
            for key in data_keys.difference(keys):
                log.debug("could not find auxiliary data for stored key '%s'", key)
    for key in keys:
        aux[key].load_data(data[key])
    return aux
