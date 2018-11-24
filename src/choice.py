"""
choice.py

A choice in a ChatNode class
"""

import re
from src import logger
from src import util

LABEL_REGEX = re.compile(r"<label>([\s\S]*?)</label>", re.MULTILINE)
COMMAND_REGEX = re.compile(r"<command>([\s\S]*?)</command>", re.MULTILINE)
TEMPLATE = """
private class Choice{id} extends Choice {{
    public Choice{id}() {{  super("{label}", "{display_text}"); }}
    public void onSelect(Conversation conversation) {{
{command_text}{next_code}
    }}}}"""


class Choice(object):
    def __init__(self, data, id):
        self.label = None
        self.text = None
        self.id = id
        self.command_text = None
        self.goto = None

        self.parse(data)

    def parse(self, data):
        # Match GOTO statements
        if "GOTO " not in data:
            raise InvalidGoto("A GOTO statement is missing for choice {}".format(self.id))

        index = data.index("GOTO ")
        self.goto = util.parse_goto(data[index:])

        # Basic checking: GOTO must be at end
        if index < util.index(data, "</label>") or \
                index < util.index(data, "</command>"):
            raise InvalidGoto("GOTO statement for choice {} must be at the end!".format(self.id))

        data = data[:index]

        # Match <label> tags
        temp = re.findall(LABEL_REGEX, data)
        if len(temp) > 1:
            raise InvalidChoice("Choice {} contains multiple ({}) <label> tags".format(self.id, len(temp)))

        self.text = data
        self.label = data

        if len(temp) > 0:
            self.label = temp[0].lstrip("\n").replace("\n", "\\n")
            self.text = data.replace("<label>{}</label>".format(temp[0]), "")

        # Match <command> tags
        temp = re.findall(COMMAND_REGEX, data)
        if len(temp) > 1:
            raise InvalidChoice("Choice {} contains multiple ({}) <command> tags".format(self.id, len(temp)))
        if len(temp) > 0:
            self.command_text = temp[0]
            self.text = data.replace("<command>{}</command>".format(self.command_text), "")
            self.label = self.label.replace("<command>{}</command>".format(self.command_text), "")

        self.text = self.text.lstrip("\n").rstrip("\n").replace("\n", "\\n")
        self.label = self.label.lstrip("\n").rstrip("\n").replace("\n", "\\n")
        self.label = self.label.replace("\\n", " ").replace("\n", " ").lstrip().rstrip()

    def generate_code(self):
        return util.indent_code(TEMPLATE.format(
            id=util.camel_case(self.id),
            label=self.label,
            display_text=self.text.lstrip().rstrip(),
            command_text=util.indent_code(self.command_text, 2) + "\n" if self.command_text is not None else "",
            next_code=util.indent_code(self.goto, 2)
        ), 2)


class InvalidGoto(Exception):
    pass


class InvalidChoice(Exception):
    pass
