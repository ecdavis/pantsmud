from unittest import TestCase

import mock

from pantsmud.driver import hook


class TestAdd(TestCase):
    def test_add_fails_with_non_callable_func(self):
        self.assertRaises(TypeError, hook.add, "test", None)


class TestRun(TestCase):
    def setUp(self):
        self.name = "test"
        self.backup_hooks = hook._hooks
        hook._hooks = {}

    def tearDown(self):
        hook._hooks = self.backup_hooks

    def test_run_non_existent_hook_does_not_fail(self):
        try:
            hook.run("foobar")
        except Exception:
            self.fail("Running a non-existent hook must not raise an exception.")

    def test_run_calls_all_functions_for_given_hook_type(self):
        func1 = mock.MagicMock()
        func1.__name__ = "func1"
        func2 = mock.MagicMock()
        func2.__name__ = "func2"
        hook.add(self.name, func1)
        hook.add(self.name, func2)
        hook.run(self.name)
        func1.assert_called_once_with(self.name)
        func2.assert_called_once_with(self.name)

    def test_run_passes_arguments_to_hook_functions(self):
        func = mock.MagicMock()
        func.__name__ = "hook"
        hook.add(self.name, func)
        hook.run(self.name, "foo", "bar", baz="omg")
        func.assert_called_once_with(self.name, "foo", "bar", baz="omg")

    def test_run_does_not_call_functions_of_other_hook_types(self):
        func1 = mock.MagicMock()
        func1.__name__ = "func1"
        func2 = mock.MagicMock()
        func2.__name__ = "func2"
        hook.add(self.name, func1)
        hook.add("other", func2)
        hook.run(self.name)
        func1.assert_called_once_with(self.name)
        self.assertEqual(func2.call_count, 0)

    def test_run_catches_exceptions_in_hook_functions(self):
        def raiser(name):
            raise Exception()

        hook.add(self.name, raiser)
        try:
            hook.run(self.name)
        except Exception:
            self.fail("hook.run must catch all exceptions in hook functions.")
