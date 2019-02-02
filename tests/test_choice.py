import unittest
from src import choice


class TestChoice(unittest.TestCase):
    def test_simple_choice_code_otuput(self):
        inp = "Choice text here GOTO id"
        out = """        
        class ChoiceId extends Choice {
            public ChoiceId() {  super("Choice text here", "Choice text here"); }
            public void onSelect(Conversation conversation) {
                conversation.gotoChatNode("id");
            }}"""
        self.assertEqual(choice.Choice(inp, "id").generate_code(), out,
                         "Testing simple choice with 'Choice text here GOTO id' and id 'id'")

    def test_choice_with_label_code_output(self):
        inp = "test\n<label>label text\nthis should be 1 line</label>\nGOTO RAND a b"
        out = """        
        class ChoiceId extends Choice {
            public ChoiceId() {  super("label text this should be 1 line", "test"); }
            public void onSelect(Conversation conversation) {
                String[] arr = {"a", "b"};
                conversation.gotoChatNode(Random.choice(arr));
            }}"""
        self.assertEqual(choice.Choice(inp, "id").generate_code(), out,
                         "Testing simple choice with 'test\\n<label>label text\\nthis should be 1 line</label>\\n" +
                         "GOTO RAND a b' and id 'id'")

    def test_choice_with_command_code_output(self):
        inp = "test\n<command>line 1\nnew line 2</command>\nGOTO RAND a b"
        out = """        
        class ChoiceId extends Choice {
            public ChoiceId() {  super("test", "test"); }
            public void onSelect(Conversation conversation) {
                line 1
                new line 2
                String[] arr = {"a", "b"};
                conversation.gotoChatNode(Random.choice(arr));
            }}"""
        self.assertEqual(choice.Choice(inp, "id").generate_code(), out,
                         "Testing simple choice with 'test\\n<command>line 1\\nnew line 2</command>\\nGOTO RAND a b")

    def test_invalid_choice_no_goto(self):
        with self.assertRaises(choice.InvalidGoto):
            choice.Choice("test\n<command>blah</command><label>blah</label>Missing GOTO", "id")

    def test_invalid_choice_goto_not_at_end(self):
        with self.assertRaises(choice.InvalidGoto):
            choice.Choice("GOTO end\ntest\n<command>blah</command><label>blah</label>Missing", "id")

    def test_invalid_choice_multiple_tags(self):
        with self.assertRaises(choice.InvalidChoice):
            choice.Choice("test\n<command>blah</command><command>blah</command>Missing GOTO id", "id")

    def test_choice_with_tags_seperating_body_text(self):
        inp = "test <command>blah</command>same line as before\nnewline GOTO id"
        out = """        
        class ChoiceId extends Choice {
            public ChoiceId() {  super("test same line as before newline", "test same line as before\\nnewline"); }
            public void onSelect(Conversation conversation) {
                blah
                conversation.gotoChatNode("id");
            }}"""
        self.assertEqual(choice.Choice(inp, "id").generate_code(), out,
                         "Testing choice with tag between: 'test <command>blah</command>same line as before\n" +
                         "newline GOTO id'")


if __name__ == '__main__':
    unittest.main()
