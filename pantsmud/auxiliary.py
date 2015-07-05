import logging

log = logging.getLogger(__name__)

AUX_TYPE_ACCOUNT = "account"
AUX_TYPE_BRAIN = "brain"
AUX_TYPE_LINK = "exit"
AUX_TYPE_MOBILE = "mobile"
AUX_TYPE_NODE = "node"
AUX_TYPE_WORLD = "world"
AUX_TYPE_ZONE = "zone"

# aux_type: {name: cls}
_auxiliary_classes = {
    AUX_TYPE_ACCOUNT: {},
    AUX_TYPE_BRAIN: {},
    AUX_TYPE_LINK: {},
    AUX_TYPE_MOBILE: {},
    AUX_TYPE_NODE: {},
    AUX_TYPE_WORLD: {},
    AUX_TYPE_ZONE: {}
}


def install(aux_type, name, cls):
    if aux_type not in _auxiliary_classes:
        log.debug("Adding new auxiliary type: '%s'", aux_type)
        _auxiliary_classes[aux_type] = {}
    assert name not in _auxiliary_classes[aux_type]
    log.debug("Adding new auxiliary class: '%s', class '%s', type '%s'", name, cls.__name__, aux_type)
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
                log.debug("Could not find stored data for auxiliary key '%s'", key)
        if len(data_keys.difference(keys)) > 0:
            for key in data_keys.difference(keys):
                log.debug("Could not find auxiliary data for stored key '%s'", key)
    for key in keys:
        aux[key].load_data(data[key])
    return aux


def save_data(aux):
    data = {}
    for key in aux.keys():
        data[key] = aux.save_data()
    return data
