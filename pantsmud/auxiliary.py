"""
A plugin implementation that allows developers to add custom data/behaviour to the core game objects without having to
modify their code.

Example of defining auxiliary data:

    class MyAux(object):
        def __init__(self):
            self.foo = "bar"

        def load_data(self, data):
            self.foo = data["bar"]

        def save_data(self):
            return {"foo": self.foo}

        def do_something(self):
            print self.foo

    auxiliary.install("baz", "my_aux", MyAux)

Example of enabling auxiliary data on a custom game object:

    class MyGameObject(object):
        def __init__(self):
            self.aux = auxiliary.new_data("baz")

        def load_data(self, data):
            self.aux = auxiliary.load_data(self.aux, data["auxiliary"]

        def save_data(self):
            return {"auxiliary": auxiliary.save_data(self.aux)}

Example of using the auxiliary data defined on the custom game object:

    def func(game_object):
        game_object.aux["my_aux"].do_something()
"""

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
    """
    Add a new auxiliary data class to the given aux_type.
    """
    if aux_type not in _auxiliary_classes:
        log.debug("Adding new auxiliary type: '%s'", aux_type)
        _auxiliary_classes[aux_type] = {}
    assert name not in _auxiliary_classes[aux_type]
    log.debug("Adding new auxiliary class: '%s', class '%s', type '%s'", name, cls.__name__, aux_type)
    _auxiliary_classes[aux_type][name] = cls


def new_data(aux_type):
    """
    Returns a dictionary containing instances of all aux data for the given aux_type.
    """
    data = {}
    if aux_type not in _auxiliary_classes:
        return data
    for name, cls in _auxiliary_classes[aux_type].iteritems():
        data[name] = cls()
    return data


def load_data(aux, data):
    """
    Loads a dictionary containing saved aux data onto the object.

    Data layout:
        {
            "my_aux_1": <dict>,  # This will be passed to aux["my_aux_1"].load_data
            "my_aux_2": <dict>  # This will be passed to aux["my_aux_2"].load_data
        }
    """
    aux_keys = set(aux.keys())
    data_keys = set(data.keys())
    keys = aux_keys.intersection(data_keys)
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
    """
    Returns a dictionary containing aux data ready to be serialized.
    """
    data = {}
    for key in aux.keys():
        data[key] = aux[key].save_data()
    return data
