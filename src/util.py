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


def is_valid_java_variable(name):
    return name[0].lower() in "abcdefghijklmnopqrstuvwxyz$_" and name not in JAVA_KEYWORDS