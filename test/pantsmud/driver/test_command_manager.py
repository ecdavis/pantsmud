import mock
import string
from unittest import TestCase
from pantsmud.driver.command import CommandManager


class TestCommandManagerAdd(TestCase):
    def setUp(self):
        self.func = lambda: None
        self.name = "test"
        self.command_manager = CommandManager(self.name)

    def test_command_exists_after_add(self):
        self.assertFalse(self.command_manager.exists(self.name))
        self.command_manager.add(self.name, self.func)
        self.assertTrue(self.command_manager.exists(self.name))

    def test_add_fails_with_no_name(self):
        self.assertRaises(TypeError, self.command_manager.add, None, self.func)
        self.assertRaises(ValueError, self.command_manager.add, '', self.func)

    def test_add_fails_with_whitespace_in_name(self):
        for c in string.whitespace:
            self.assertRaises(ValueError, self.command_manager.add, self.name + c + self.name, self.func)

    def test_add_fails_with_no_func(self):
        self.assertRaises(TypeError, self.command_manager.add, self.name, None)

    def test_add_fails_with_non_callable_func(self):
        self.assertRaises(TypeError, self.command_manager.add, self.name, "foobar")


class TestCommandManagerRun(TestCase):
    def setUp(self):
        self.func = lambda: None
        self.name = "test"
        self.command_manager = CommandManager(self.name)

    def test_command_function_is_called_by_run(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        actor = mock.MagicMock()
        self.command_manager.add(self.name, func)

        self.command_manager.run(actor, self.name, None)
        func.assert_called_once_with(actor, self.name, None)

    def test_run_fails_if_command_does_not_exist(self):
        actor = mock.MagicMock()
        self.assertRaises(KeyError, self.command_manager.run, actor, self.name, None)

    def test_run_fails_with_no_actor(self):
        self.command_manager.add(self.name, self.func)

        self.assertRaises(TypeError, self.command_manager.run, None, self.name, None)

    def test_run_fails_when_actor_has_no_environment(self):
        self.command_manager.add(self.name, self.func)
        actor = mock.MagicMock()
        actor.environment = None

        self.assertRaises(ValueError, self.command_manager.run, actor, self.name, None)

    def test_run_suppresses_exceptions_in_command_func(self):
        def raiser(actor, cmd, args):
            raise Exception()
        actor = mock.MagicMock()
        self.command_manager.add(self.name, raiser)

        try:
            self.command_manager.run(actor, self.name, "")
        except Exception:
            self.fail("CommandManager.run must catch all exceptions raised by command functions.")


class TestCommandManagerInputHandler(TestCase):
    def setUp(self):
        self.func = lambda: None
        self.name = "test"
        self.command_manager = CommandManager(self.name)

    def test_command_function_is_called_by_input_handler(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        actor = mock.MagicMock()
        self.command_manager.add(self.name, func)

        self.command_manager.input_handler(actor, self.name)
        func.assert_called_once_with(actor, self.name, '')

    def test_input_handler_does_not_run_command_with_no_input(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        self.command_manager.input_handler(None, None)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the input is None.")
        self.command_manager.input_handler(None, "")
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the input is an empty string.")

    def test_input_handler_does_not_run_command_with_only_whitespace_input(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        self.command_manager.input_handler(None, string.whitespace)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the input is only whitespace.")

    def test_input_handler_does_not_run_command_when_input_begins_with_whitespace(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        for c in string.whitespace:
            self.command_manager.input_handler(mock.MagicMock(), c + self.name)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the first character is whitespace.")

    def test_input_handler_does_not_run_command_when_input_begins_with_digit(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        for c in string.digits:
            self.command_manager.input_handler(mock.MagicMock(), c + self.name)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the first character is a digit.")

    def test_input_handler_does_not_run_command_when_input_begins_with_punctuation(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        for c in string.punctuation:
            self.command_manager.input_handler(mock.MagicMock(), c + self.name)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the first character is a digit.")

    def test_input_handler_does_not_run_command_when_input_contains_invalid_characters(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        self.command_manager.add(self.name, func)

        line = self.name + " foo\t\r\n\tbar"
        self.command_manager.input_handler(mock.MagicMock(), line)
        self.assertEqual(func.call_count, 0, "CommandManager.input_handler must not run a command if the input contains invalid characters.")

    def test_input_handler_strips_whitespace_and_runs_command_when_input_ends_with_whitespace(self):
        func = mock.MagicMock()
        func.__name__ = "func"
        actor = mock.MagicMock()
        self.command_manager.add(self.name, func)

        self.command_manager.input_handler(actor, self.name + string.whitespace)
        func.assert_called_once_with(actor, self.name, '')

    def test_input_handler_sends_message_on_invalid_input(self):
        actor = mock.MagicMock()
        self.command_manager.input_handler(actor, "foobar\t")
        self.assertEqual(actor.message.call_count, 1, "CommandManager.input_handler must message the actor if the input is invalid.")
        self.command_manager.input_handler(actor, "\tfoobar")
        self.assertEqual(actor.message.call_count, 2, "CommandManager.input_handler must message the actor if the input is invalid.")

    def test_input_handler_sends_command_notfound_message(self):
        actor = mock.MagicMock()
        self.command_manager.input_handler(actor, "foobar")
        self.assertEqual(actor.message.call_count, 1, "CommandManager.input_handler must message the actor if the command is not found.")

    def test_input_handler_splits_command_name_from_arguments(self):
        actor = mock.MagicMock()
        cmd = self.name
        args = "foo bar baz bar"
        line = cmd + " " + args
        func = mock.MagicMock()
        func.__name__ = func
        self.command_manager.add(self.name, func)

        self.command_manager.input_handler(actor, line)
        func.assert_called_once_with(actor, cmd, args)
