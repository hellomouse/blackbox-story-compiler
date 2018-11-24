import unittest
from src import util


class TestUtil(unittest.TestCase):
    def test_is_valid_java_variable_names(self):
        good_names = [
            "variable",
            "word123",
            "_test",
            "$code",
            "cool_name",
            "variableName",
            "VariableName",
            "VARIABLE_NAME"
        ]
        bad_names = [
            "123word",
            "final",
            "static",
            "variable name",
            "INVALID*NAME",
            ""
        ]

        for name in good_names:
            self.assertEqual(util.is_valid_java_variable(name), True, "Valid Java variable tested: '{}'".format(name))
        for name in bad_names:
            self.assertEqual(util.is_valid_java_variable(name), False, "Invalid Java variable tested: '{}'".format(name))

    def test_indent_lines_with_4_spaces_once(self):
        self.assertEqual(util.indent_code("test code\n    indent this", 1),
                         "    test code\n        indent this",
                         "Testing indenting of 'test code\n    indent this' with 4 spaces")

    def test_string_with_spaces_between_to_titled_camel_case(self):
        test_map = {
            "test word": "TestWord",
            "a b c 1": "ABC1"
        }
        for initial, final in test_map.items():
            self.assertEqual(util.camel_case(initial), final, "Camel casing '{}'".format(initial))

    def test_parse_goto(self):
        part_2_correct = "String[] arr = {\"a\", \"b\", \"c\"};\n" + \
                         "conversation.gotoChatNode(Random.choice(arr));"
        part_3_correct = "java code\njava code\njava code"

        self.assertEqual(util.parse_goto("GOTO id"), "conversation.gotoChatNode(\"id\");", "Testing simple 'GOTO id' syntax")
        self.assertEqual(util.parse_goto("GOTO RAND a b c"), part_2_correct, "Testing 'GOTO RAND a b c' syntax")
        self.assertEqual(util.parse_goto("GOTO CODE java code\njava code\njava code<endcode>"),
                         part_3_correct, "Testing 'GOTO CODE ... <endcode>' syntax")

    def test_util_index_of_return_minus_1_if_missing(self):
        s = "0123456780"
        self.assertEqual(util.index(s, "0"), 0, "Index of '0' should be 0")
        self.assertEqual(util.index(s, "7"), 7, "Index of '7' should be 7")
        self.assertEqual(util.index(s, "abc"), -1, "Index of 'abc' should be -1")


if __name__ == '__main__':
    unittest.main()
