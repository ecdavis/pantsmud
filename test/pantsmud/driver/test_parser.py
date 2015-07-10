from unittest import TestCase

from pantsmud.driver import command, parser


class TestParse(TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    def test_parse_works_for_one_word(self):
        pattern = [("foo", parser.WORD)]
        token_string = "bar"
        expected = {
            "foo": "bar"
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_works_for_one_int(self):
        pattern = [("foo", parser.INT)]
        token_string = "123"
        expected = {
            "foo": 123
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_works_for_one_string(self):
        pattern = [("foo", parser.STRING)]
        token_string = "foo bar 123 hello world"
        expected = {
            "foo": "foo bar 123 hello world"
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_works_for_word_int_and_string(self):
        pattern = [("foo", parser.WORD), ("bar", parser.INT), ("baz", parser.STRING)]
        token_string = "abc 123 hello 987 world"
        expected = {
            "foo": "abc",
            "bar": 123,
            "baz": "hello 987 world"
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_words_for_word_int_and_string_with_variable_length_whitespace(self):
        pattern = [("foo", parser.WORD), ("bar", parser.INT), ("baz", parser.STRING)]
        token_string = "abc   123  hello    987  world"
        expected = {
            "foo": "abc",
            "bar": 123,
            "baz": "hello    987  world"
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_works_with_leading_whitespace(self):
        pattern = [("foo", parser.WORD)]
        token_string = "   bar"
        expected = {
            "foo": "bar"
        }
        self.assertDictEqual(expected, self.parser.parse(pattern, token_string))

    def test_parse_raises_PatternError_if_token_type_does_not_exist(self):
        pattern = [("foo", "bar")]
        token_string = "baz"
        self.assertRaises(parser.PatternError, self.parser.parse, pattern, token_string)

    def test_parse_raises_CommandError_if_int_param_is_not_an_int(self):
        pattern = [("foo", parser.INT)]
        token_string = "bar"
        self.assertRaises(command.CommandError, self.parser.parse, pattern, token_string)

    def test_parse_raises_CommandError_if_pattern_has_rules_but_token_string_is_only_whitespace(self):
        pattern = [("foo", parser.WORD)]
        token_string = "    "
        self.assertRaises(command.CommandError, self.parser.parse, pattern, token_string)

    def test_parse_raises_CommandError_if_number_of_params_is_less_than_length_of_pattern(self):
        pattern = [("foo", parser.WORD), ("bar", parser.WORD)]
        token_string = "baz"
        self.assertRaises(command.CommandError, self.parser.parse, pattern, token_string)

    def test_parse_raises_CommandError_if_number_of_params_is_greater_than_length_of_pattern(self):
        pattern = [("foo", parser.WORD)]
        token_string = "bar baz"
        self.assertRaises(command.CommandError, self.parser.parse, pattern, token_string)


class TestAddTokenType(TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    def test_add_token_type_raises_TypeError_when_type_func_is_not_callable(self):
        self.assertRaises(TypeError, self.parser.add_token_type, "test", None)
