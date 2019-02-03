"""
chatnode.py

A chatnode class to be rendered
into the constructor
"""

import re
from src import logger
from src import choice
from src import util
import uuid

CHOICE_REGEX = re.compile(r"<choice>([\s\S]*?)</choice>", re.MULTILINE)
TIMEOUT_REGEX = re.compile(r"<timeout>([\s\S]*?)</timeout>", re.MULTILINE)
COMMAND_REGEX = re.compile(r"<command>([\s\S]*?)</command>", re.MULTILINE)

TEMPLATE = """{choice_classes}

class ChatNode{id} extends ChatNode {{
    public ChatNode{id}() {{
        super(generateChoices(), "{text}", {timeout}, {timeout_choice});
    }}
    
    private static Array<Choice> generateChoices() {{
        Array<Choice> choices = new Array<Choice>();
        {choice_adding}
        return choices;
    }}
    
    public void onLoad(Conversation conversation) {{
        super.onLoad(conversation);{on_load_code}
    }}
}}"""

id_counter = 0


def get_next_id(node_id):
    global id_counter
    id_counter += 1
    return node_id + str(id_counter)


class ChatNode(object):
    """
    Init a chatnode object. Note: data is a string
    array of individual lines.
    """
    def __init__(self, data):
        self.id = None
        self.command_choice = ""
        self.timeout = -1
        self.timeout_choice = None
        self.choices = []
        self.text = None
        self.uuid = uuid.uuid4().hex

        self.parse(data)
        self.parse_text(data)

    def parse(self, data):
        self.parse_header(data)

        data = "\n".join(data)
        self.parse_choice(data)
        self.parse_timeout(data)

        temp = re.findall(COMMAND_REGEX, data)
        self.command_choice = "" if len(temp) == 0 else temp[0]

        if len(temp) > 1:
            logger.log.warn("Multiple matches detected for <command> in Chatnode ID {}".format(self.id))

    def parse_header(self, data):
        header_info = data[0].split(" ")
        if header_info[0] != "CHATNODE" or len(header_info) < 2:
            raise InvalidChatNode("Chat node with header {} contains invalid CHATNODE header".format(data[0]))

        self.id = header_info[1] + self.uuid
        self.timeout = -1 if len(header_info) <= 2 else header_info[2]

        try:
            self.timeout = int(self.timeout)
        except Exception as e:
            print("Timeout in chatnode with header {} is invalid (Must be int (ms))".format(data[0]))
            raise e

    def parse_choice(self, data):
        # Match choices in <choice>...</choice> tags
        self.choices = [choice.Choice(c, get_next_id(self.id)) for c in re.findall(CHOICE_REGEX, data)]

        # Match choices defined like - ... GOTO
        for line in data.split("\n"):
            if line.startswith("- ") and " GOTO" in line:
                self.choices.append(choice.Choice(line[2:].replace(" GOTO", "\nGOTO"), get_next_id(self.id)))

    def parse_timeout(self, data):
        temp = re.findall(TIMEOUT_REGEX, data)
        if len(temp) == 0 and self.timeout > -1:
            raise InvalidChatNode("Chatnode ID: {} is missing a <timeout> tag when timeout is defined".format(self.id))
        if len(temp) > 0 > self.timeout:
            logger.log.warn("A <timeout> tag was defined for choice id {}".format(self.id))
            logger.log.warn("But no timeout was specified in the CHATNODE header.")
            logger.log.warn("(Syntax: CHATNODE id timeout(ms))")
        if len(temp) > 1:
            logger.log.warn("Multiple <timeout> tags detected in ChatNode id {}".format(self.id))
            logger.log.warn("(There should only be one!)")
        if len(temp) > 0:
            self.timeout_choice = choice.Choice(temp[0], get_next_id(self.id))

    def generate_choice_classes(self):
        arr = self.choices if self.timeout_choice is None else self.choices + [self.timeout_choice]
        return " ".join([c.generate_code() for c in arr])

    def generate_choice_adding(self):
        return util.indent_code("\n".join(["choices.add(new Choice{}());".format(c.id)
                                          for c in self.choices]), 2)

    def parse_text(self, data):
        data = "\n".join(data[1:])
        for c in re.findall(CHOICE_REGEX, data):
            data = data.replace("<choice>" + c + "</choice>", "")
        for c in re.findall(TIMEOUT_REGEX, data):
            data = data.replace("<timeout>" + c + "</timeout>", "")
        for c in re.findall(COMMAND_REGEX, data):
            data = data.replace("<command>" + c + "</command>", "")
        data = "\n".join([x for x in data.split("\n") if not (x.startswith("- ") and "GOTO " in x)])
        self.text = data.replace("\n", " ").lstrip().rstrip()

    def generate_code(self):
        tc = "null" if self.timeout_choice is None else "new Choice{}()".format(self.timeout_choice.id)
        return util.indent_code(TEMPLATE.format(
            id=util.camel_case(self.id),
            choice_classes=self.generate_choice_classes(),
            choice_adding=self.generate_choice_adding(),
            text=self.text,
            timeout=self.timeout if self.timeout is not None else "-1",
            timeout_choice=tc,
            on_load_code="\n" + self.command_choice if self.command_choice != "" else ""
        ), 2)


class InvalidChatNode(Exception):
    pass
