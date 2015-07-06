import mock
from unittest import TestCase

from pantsmud import hook, error
from pantsmud.user import session


class TestSessionClass(TestCase):
    def setUp(self):
        self.session = session.Session(mock.MagicMock())
        self.mobile = mock.MagicMock()
        self.session.world = mock.MagicMock()
        self.session.world.mobiles = {self.mobile.uuid: self.mobile}
        self.ih = mock.MagicMock()
        self.state = mock.MagicMock()

    def test_is_user(self):
        self.assertTrue(self.session.is_user)

    def test_mobile(self):
        self.session.mobile_uuid = self.mobile.uuid
        self.assertEqual(self.session.mobile, self.mobile)

    def test_mobile_when_uuid_is_none(self):
        self.session.mobile_uuid = None
        self.assertIsNone(self.session.mobile)

    def test_set_mobile(self):
        self.session.mobile = self.mobile
        self.assertEqual(self.session.mobile_uuid, self.mobile.uuid)

    def test_set_mobile_to_none(self):
        self.session.mobile = None
        self.assertIsNone(self.session.mobile_uuid)

    def test_input_handler(self):
        self.session.input_handlers.append((self.ih, None))
        self.assertEqual(self.ih, self.session.input_handler)

    def test_input_handler_fails_when_none_added(self):
        self.assertRaises(error.BrainMissingInputHandlers, getattr, self.session, "input_handler")

    def test_state(self):
        self.session.input_handlers.append((None, self.state))
        self.assertEqual(self.state, self.session.state)

    def test_state_fails_when_none_added(self):
        self.assertRaises(error.BrainMissingInputHandlers, getattr, self.session, "state")

    def test_push_input_handler(self):
        self.session.push_input_handler(self.ih, self.state)
        self.assertEqual(self.ih, self.session.input_handler)
        self.assertEqual(self.state, self.session.state)

    def test_pop_input_handler(self):
        self.session.push_input_handler(self.ih, self.state)
        ih, state = self.session.pop_input_handler()
        self.assertEqual(ih, self.ih)
        self.assertEqual(state, self.state)

    def test_pop_input_handler_fails_when_none_added(self):
        self.assertRaises(error.BrainMissingInputHandlers, self.session.pop_input_handler)


class TestSessionFunctions(TestCase):
    def setUp(self):
        self.open_brain_hook = mock.MagicMock()
        self.open_brain_hook.__name__ = "open_brain_hook"
        self.close_brain_hook = mock.MagicMock()
        self.close_brain_hook.__name__ = "close_brain_hook"
        hook.add(hook.HOOK_OPEN_BRAIN, self.open_brain_hook)
        hook.add(hook.HOOK_CLOSE_BRAIN, self.close_brain_hook)

    def test_open_session(self):
        stream = mock.MagicMock()
        sess = session.open_session(stream)
        self.assertEqual(sess.stream, stream)
        self.open_brain_hook.assert_called_once_with(hook.HOOK_OPEN_BRAIN, sess)

    def test_close_session(self):
        stream = mock.MagicMock()
        sess1 = session.open_session(stream)
        sess2 = session.close_session(stream)
        self.assertEqual(sess1, sess2)
        self.close_brain_hook.assert_called_once_with(hook.HOOK_CLOSE_BRAIN, sess1)

    def test_get_session_after_open(self):
        stream = mock.MagicMock()
        self.assertRaises(KeyError, session.get_session, stream)
        sess1 = session.open_session(stream)
        sess2 = session.get_session(stream)
        self.assertEqual(sess1, sess2)

    def test_get_session_fails_after_close(self):
        stream = mock.MagicMock()
        session.open_session(stream)
        session.close_session(stream)
        self.assertRaises(KeyError, session.get_session, stream)
