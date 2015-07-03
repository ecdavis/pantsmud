import glob
import json
import os.path


def read(path):
    with open(path, 'r') as f:
        return json.load(f)


def write(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def load_files(path, pattern, cls):
    if not os.path.exists(path):
        raise IOError("Path not found: '%s'" % path)
    if not os.path.isdir(path):
        raise IOError("Path is not directory: '%s'" % path)
    files = glob.glob("%s/%s" % (path, pattern))
    return [load_file(f, cls) for f in files]


def load_file(path, cls):
    if not os.path.exists(path):
        raise IOError("Path not found: '%s'" % path)
    if not os.path.isfile(path):
        raise IOError("Path is not a file: '%s'" % path)
    data = read(path)
    obj = cls()
    obj.load_data(data)
    return obj
