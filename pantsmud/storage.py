"""
A collection of functions to enable saving/loading of arbitrary game objects to/from disk.
"""

import glob
import json
import logging
import os.path


log = logging.getLogger(__name__)


def load(path):
    """
    Read and deserialize data from a file.
    """
    with open(path, 'r') as f:
        return json.load(f)


def load_files(path, pattern, cls):
    """
    Load game objects from all files under the given path.

    Calls load_file for all files under the given path that match the given pattern. See glob.glob documentation for
    pattern format details.
    """
    if not os.path.exists(path):
        raise IOError("Path not found: '%s'" % path)
    if not os.path.isdir(path):
        raise IOError("Path is not directory: '%s'" % path)
    files = glob.glob("%s/%s" % (path, pattern))
    return [load_file(f, cls) for f in files]


def load_file(path, cls):
    """
    Load a game object from a file.

    Creates a new instance of the given class, then calls cls.load_data with the deserialized data from the file.
    """
    if not os.path.exists(path):
        raise IOError("Path not found: '%s'" % path)
    if not os.path.isfile(path):
        raise IOError("Path is not a file: '%s'" % path)
    data = load(path)
    obj = cls()
    obj.load_data(data)
    return obj


def save(path, data):
    """
    Serialize and write data to a file.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def save_objects(path, extension, objs):
    """
    Save game objects to files with the given extension under the given path.

    For each file, creates a file path from the given directory path, extension and obj.name. The file path and obj are
    then passed to save_object.
    """
    if not os.path.exists(path):
        raise IOError("Path not found: '%s'" % path)
    if not os.path.isdir(path):
        raise IOError("Path is not directory: '%s'" % path)
    for obj in objs:
        obj_path = "%s/%s%s" % (path, obj.name, extension)
        save_object(obj_path, obj)


def save_object(path, obj):
    """
    Save a game object to a file.

    Calls obj.save_data and then passes the data to save.
    """
    if os.path.exists(path):
        if not os.path.isfile(path):
            raise IOError("Path is not a file: '%s'" % path)
        log.debug("Overwriting file: '%s'", path)
    data = obj.save_data()
    save(path, data)
