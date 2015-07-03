import glob
import json
import os.path


def read(path):
    if not os.path.exists(path):
        raise Exception("TODO")  # TODO
    with open(path, 'r') as f:
        return json.load(f)


def write(path, data):
    if not os.path.exists(path):
        raise Exception("TODO")  # TODO
    with open(path, 'w') as f:
        json.dump(data, f)


def load_files(path, pattern, cls):
    if not os.path.exists(path):
        raise Exception("TODO")  # TODO
    if not os.path.isdir(path):
        raise Exception("TODO")  # TODO
    files = glob.glob("%s/%s" % (path, pattern))
    for f in files:
        obj = load_file(f, cls)  # TODO try/except
        yield obj


def load_file(path, cls):
    if not os.path.exists(path):
        raise Exception("TODO")  # TODO
    if not os.path.isfile(path):
        raise Exception("TODO")  # TODO
    data = read(path)  # TODO try/except
    o = cls()
    o.load_data(data)  # TODO try/except
    return o
