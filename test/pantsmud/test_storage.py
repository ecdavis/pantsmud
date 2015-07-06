import glob
import os
import os.path

import mock
from unittest import TestCase

from pantsmud import storage


def check_and_remove(path):
    if os.path.exists(path):
        os.remove(path)


class Obj(object):
    def __init__(self):
        self.load_data = mock.MagicMock()


class TestSaveAndLoad(TestCase):
    def setUp(self):
        self.d1 = {"key1": "value1", "key2": "value2"}
        self.path = os.path.join(os.path.dirname(__file__), "test.json")
        check_and_remove(self.path)

    def tearDown(self):
        check_and_remove(self.path)

    def test_save_and_load_keeps_data_intact(self):
        storage.save(self.path, self.d1)
        d2 = storage.load(self.path)
        self.assertDictEqual(self.d1, d2)

    def test_save_creates_file(self):
        self.assertFalse(os.path.exists(self.path))
        storage.save(self.path, self.d1)
        self.assertTrue(os.path.exists(self.path))


class TestLoadFile(TestCase):
    def setUp(self):
        self.d1 = {"key1": "value1", "key2": "value2"}
        self.path1 = os.path.join(os.path.dirname(__file__), "test1.json")
        self.path2 = os.path.join(os.path.dirname(__file__), "test2.json")
        check_and_remove(self.path1)
        storage.save(self.path1, self.d1)
        check_and_remove(self.path2)

    def tearDown(self):
        check_and_remove(self.path1)
        check_and_remove(self.path2)

    def test_load_file(self):
        obj = storage.load_file(self.path1, Obj)
        self.assertTrue(isinstance(obj, Obj))
        obj.load_data.assert_called_once_with(self.d1)

    def test_load_file_fails_if_path_does_not_exist(self):
        self.assertRaises(IOError, storage.load_file, self.path2, None)

    def test_load_file_fails_if_path_exists_but_is_a_directory(self):
        self.assertRaises(IOError, storage.load_file, os.path.dirname(self.path1), None)


class TestLoadFiles(TestCase):
    def setUp(self):
        self.d1 = {"key1": "value1", "key2": "value2"}
        self.d2 = {"key3": "value3", "key4": "value4"}
        self.d3 = {"key5": "value5", "key6": "value6"}
        self.d4 = {"key7": "value7", "key8": "value8"}
        self.path1 = os.path.join(os.path.dirname(__file__), "test1.foo.json")
        self.path2 = os.path.join(os.path.dirname(__file__), "test2.foo.json")
        self.path3 = os.path.join(os.path.dirname(__file__), "test3.bar.json")
        self.path4 = os.path.join(os.path.dirname(__file__), "test4.bar.json")
        check_and_remove(self.path1)
        storage.save(self.path1, self.d1)
        check_and_remove(self.path2)
        storage.save(self.path2, self.d2)
        check_and_remove(self.path3)
        storage.save(self.path3, self.d3)
        check_and_remove(self.path4)
        storage.save(self.path4, self.d4)

    def tearDown(self):
        check_and_remove(self.path1)
        check_and_remove(self.path2)
        check_and_remove(self.path3)
        check_and_remove(self.path4)

    def test_load_files(self):
        objs = storage.load_files(os.path.dirname(self.path1), "*.foo.json", Obj)
        self.assertEqual(len(objs), 2)
        for obj, data in zip(objs, [self.d1, self.d2]):
            self.assertTrue(isinstance(obj, Obj))
            obj.load_data.assert_called_once_with(data)

    def test_load_files_fails_if_path_does_not_exist(self):
        self.assertRaises(IOError, storage.load_files, os.path.join(os.getcwd(), r"path\does\not\exist"), None, None)

    def test_load_files_fails_if_path_exists_but_is_not_a_directory(self):
        self.assertRaises(IOError, storage.load_files, self.path1, None, None)


class TestSaveObject(TestCase):
    def setUp(self):
        self.d1 = {"key1": "value1", "key2": "value2"}
        self.obj = Obj()
        self.obj.save_data = mock.Mock(return_value=self.d1)
        self.path = os.path.join(os.path.dirname(__file__), "test.json")
        check_and_remove(self.path)

    def tearDown(self):
        check_and_remove(self.path)

    def test_save_object(self):
        storage.save_object(self.path, self.obj)
        self.assertTrue(os.path.exists(self.path))
        data = storage.load(self.path)
        self.assertDictEqual(data, self.d1)

    def test_save_object_overwrites_files(self):
        storage.save(self.path, {})
        self.assertTrue(os.path.exists(self.path))
        self.test_save_object()

    def test_save_object_fails_if_path_is_a_directory(self):
        self.assertRaises(IOError, storage.save_object, os.path.dirname(self.path), None)


class TestSaveObjects(TestCase):
    def setUp(self):
        self.d1 = {"key1": "value1", "key2": "value2"}
        self.d2 = {"key3": "value3", "key4": "value4"}
        self.obj1 = Obj()
        self.obj1.name = "test1"
        self.obj1.save_data = mock.Mock(return_value=self.d1)
        self.obj2 = Obj()
        self.obj2.name = "test2"
        self.obj2.save_data = mock.Mock(return_value=self.d2)
        self.path = os.path.dirname(__file__)
        self.extension = ".test.json"

    def tearDown(self):
        for path in glob.glob("%s/%s" % (self.path, '*'+self.extension)):
            check_and_remove(path)

    def test_save_objects(self):
        objs = [self.obj1, self.obj2]
        storage.save_objects(self.path, self.extension, objs)
        for obj, data in zip(objs, [self.d1, self.d2]):
            path = "%s/%s%s" % (self.path, obj.name, self.extension)
            self.assertTrue(os.path.exists(path))
            loaded_data = storage.load(path)
            self.assertDictEqual(data, loaded_data)

    def test_save_objects_fails_if_path_does_not_exist(self):
        self.assertRaises(IOError, storage.save_objects, os.path.join(os.getcwd(), r"path\does\not\exist"), None, None)

    def test_save_objects_fails_if_path_exists_but_is_not_a_directory(self):
        self.assertRaises(IOError, storage.save_objects, __file__, None, None)
