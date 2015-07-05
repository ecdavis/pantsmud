"""
A collection of functions to enable saving/loading of arbitrary game objects to/from disk.
"""

import glob
import json
import os.path


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
        json.dump(data, f)
