"""
util.py
"""

JAVA_KEYWORDS = ["abstract",  "assert",       "boolean",    "break",      "byte",      "case",
                 "catch",     "char",         "class",      "const",     "continue",
                 "default",   "do",           "double",     "else",      "extends",
                 "false",     "final",        "finally",    "float",     "for",
                 "goto",      "if",           "implements", "import",    "instanceof",
                 "int",       "interface",    "long",       "native",    "new",
                 "null",      "package",      "private",    "protected", "public",
                 "return",    "short",        "static",     "strictfp",  "super",
                 "switch",    "synchronized", "this",       "throw",     "throws",
                 "transient", "true",         "try",        "void",      "volatile",
                 "while"]
TAB_SPACE = 4


def is_valid_java_variable(name):
    return len(name) > 0 and name.lower()[0] in "abcdefghijklmnopqrstuvwxyz$_" and \
        all([char in "abcdefghijklmnopqrstuvwxyz$_1234567890" for char in name.lower()]) and name not in JAVA_KEYWORDS


def indent_code(string, tabs):
    return "\n".join([" " * (TAB_SPACE * tabs) + line for line in string.split("\n")])


def camel_case(string):
    return "".join([x.title() for x in string.split(" ")])


def parse_goto(line):
    line = line.split("GOTO ")[1]

    # Randomization: RAND choice1 choice2...
    if line.split(" ")[0] == "RAND":
        return "String[] arr = {" + ", ".join(["\"{}\"".format(x.replace("\n", "")) for x in line.split(" ")[1:]]) + "};\n" + \
               "conversation.gotoChatNode(Random.choice(arr));"

    # Embed java code
    if line.split(" ")[0] == "CODE":
        return line.split("CODE ")[1].split("<endcode>")[0]

    # Normal GOTO (GOTO id)
    return "conversation.gotoChatNode(\"" + line.replace("\n", "") + "\");"


def index(string, search):
    try:
        return string.index(search)
    except ValueError:
        return -1
