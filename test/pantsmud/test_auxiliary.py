import mock
from unittest import TestCase

from pantsmud import auxiliary


class Aux(object):
    def __init__(self):
        self.load_data = mock.MagicMock()
        self.save_data = mock.Mock(return_value=self.__class__.__name__)


class Aux1(Aux):
    pass


class Aux2(Aux):
    pass


class TestNewData(TestCase):
    def setUp(self):
        self.backup_auxiliary = auxiliary._auxiliary_classes
        auxiliary._auxiliary_classes = {}
        self.aux_type_1 = "test_aux_type_1"
        self.aux_type_2 = "test_aux_type_2"
        self.name_1 = "test_aux_1"
        self.name_2 = "test_aux_2"

    def tearDown(self):
        auxiliary._auxiliary_classes = self.backup_auxiliary

    def test_new_data_returns_a_dict_containing_all_installed_classes(self):
        auxiliary.install(self.aux_type_1, self.name_1, Aux1)
        auxiliary.install(self.aux_type_1, self.name_2, Aux2)
        data = auxiliary.new_data(self.aux_type_1)
        self.assertTrue(isinstance(data[self.name_1], Aux1))
        self.assertTrue(isinstance(data[self.name_2], Aux2))

    def test_new_data_does_not_instantiate_classes_installed_on_other_types(self):
        auxiliary.install(self.aux_type_1, self.name_1, Aux1)
        auxiliary.install(self.aux_type_2, self.name_2, Aux2)
        data = auxiliary.new_data(self.aux_type_1)
        self.assertTrue(isinstance(data[self.name_1], Aux1))
        self.assertFalse(self.name_2 in data)
        self.assertEqual(len(data), 1)

    def test_new_data_does_not_instantiate_classes_with_same_name_installed_on_other_types(self):
        auxiliary.install(self.aux_type_1, self.name_1, Aux1)
        auxiliary.install(self.aux_type_2, self.name_1, Aux2)
        data = auxiliary.new_data(self.aux_type_1)
        self.assertTrue(isinstance(data[self.name_1], Aux1))
        self.assertEqual(len(data), 1)
        data = auxiliary.new_data(self.aux_type_2)
        self.assertTrue(isinstance(data[self.name_1], Aux2))
        self.assertEqual(len(data), 1)

    def test_new_data_returns_empty_dict_when_aux_type_does_not_exist(self):
        data = auxiliary.new_data(self.aux_type_1)
        self.assertEqual(len(data), 0)


class TestLoadData(TestCase):
    def setUp(self):
        self.backup_auxiliary = auxiliary._auxiliary_classes
        auxiliary._auxiliary_classes = {}
        self.type_1 = "test_aux_type_1"
        self.name_1 = "test_aux_1"
        self.name_2 = "test_aux_2"
        self.name_3 = "test_aux_3"
        self.data_1 = {"key_1": "value_1"}
        self.data_2 = {"key_2": "value_2"}
        self.data_3 = {"key_3": "value_3"}
        auxiliary.install(self.type_1, self.name_1, Aux1)

    def tearDown(self):
        auxiliary._auxiliary_classes = self.backup_auxiliary

    def test_load_data_passed_each_aux_classes_data_to_its_load_data_method(self):
        auxiliary.install(self.type_1, self.name_2, Aux2)

        aux = auxiliary.new_data(self.type_1)

        auxiliary.load_data(aux, {self.name_1: self.data_1, self.name_2: self.data_2})
        aux[self.name_1].load_data.assert_called_once_with(self.data_1)
        aux[self.name_2].load_data.assert_called_once_with(self.data_2)

    def test_load_data_ignores_missing_data(self):
        auxiliary.install(self.type_1, self.name_2, Aux2)

        aux = auxiliary.new_data(self.type_1)

        auxiliary.load_data(aux, {self.name_1: self.data_1})
        aux[self.name_1].load_data.assert_called_once_with(self.data_1)
        self.assertEqual(aux[self.name_2].load_data.call_count, 0)

    def test_load_data_ignores_extra_data(self):
        aux = auxiliary.new_data(self.type_1)

        auxiliary.load_data(aux, {self.name_1: self.data_1, self.name_3: self.data_3})
        aux[self.name_1].load_data.assert_called_once_with(self.data_1)
        self.assertEqual(len(aux), 1)


class TestSaveData(TestCase):
    def setUp(self):
        self.backup_auxiliary = auxiliary._auxiliary_classes
        auxiliary._auxiliary_classes = {}
        auxiliary.install("test_aux_type", "test_aux_1", Aux1)
        auxiliary.install("test_aux_type", "test_aux_2", Aux2)
        self.aux = auxiliary.new_data("test_aux_type")

    def tearDown(self):
        auxiliary._auxiliary_classes = self.backup_auxiliary

    def test_save_data_returns_a_dict_containing_saved_data_from_all_instances(self):
        data = auxiliary.save_data(self.aux)
        for key, val in data.items():
            self.assertEqual(val, self.aux[key].save_data())
