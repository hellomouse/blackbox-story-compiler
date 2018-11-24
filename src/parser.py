"""
Parser.py

Parses a string containing the blackbox story
code into a Conversation object
"""

from src import logger
from src import util
from src import chatnode


stop_lines = [
    "SCENE", "SCENE_SUB", "SOUND", "MUSIC", "SCENE_BACKGROUND",
    "DEFINE", "DEFINE_GLOBAL", "CHATNODE", "SCENE_START", "SCENE_END"
]
CLASS_TEMPLATE = """
package blackbox.game.conversation.story;

import com.badlogic.gdx.Screen;
import com.badlogic.gdx.audio.Music;
import com.badlogic.gdx.audio.Sound;
import com.badlogic.gdx.utils.ObjectMap;

import blackbox.game.util.*;
import blackbox.game.conversation.graph.*;

public class {classname} extends Conversation {{
    public {classname}(Screen level) {{
        super(level, "{title}", "{subtitle}", "{background}");
        {music_code}{sound_code}{variable_code}
        /* Generate classes */
{class_code}
{add_chatnode_code}
    }}

    public void gotoStart() {{
{go_to_start}
    }}
}}
"""


class Parser(object):
    def __init__(self, string):
        self.lines = list(filter(lambda x: not x.startswith("#"), string.split("\n")))
        self.lines = [line.lstrip().rstrip() for line in self.lines]

        # Basic metadata
        self.title = None
        self.subtitle = None
        self.sounds = []
        self.musics = []
        self.background_id = "default"
        self.variables = []
        self.start = None
        self.class_name = None

        # Advanced metadata
        self.chatnodes = []

        # Do initial parsing
        self.parse_basic()
        self.parse_chatnodes()

    """
    parse)basic - Scans the string
    for basic metadata like conversation
    title, subtitle, etc...
    """
    def parse_basic(self):
        scene_start_found = False
        scene_end_found = False

        for index, line in enumerate(self.lines):
            if line.startswith("SCENE "):
                if self.title is not None:
                    logger.log.warn("A scene title has already been defined, overriding")
                    logger.log.warn("See line {}: {}".format(index + 1, self.title))
                self.title = line.split(" ", 1)[1]
            elif line.startswith("SCENE_SUB "):
                if self.subtitle is not None:
                    logger.log.warn("A scene subtitle has already been defined, overriding")
                    logger.log.warn("See line {}: {}".format(index + 1, self.subtitle))
                self.subtitle = line.split(" ", 1)[1]
            elif line.startswith("SCENE_BACKGROUND "):
                self.background_id = line.split(" ", 1)[1]
            elif line.startswith("SOUND "):
                self.sounds.append(line.split(" ", 1)[1].rsplit(" ", 1))
            elif line.startswith("MUSIC "):
                self.musics.append(line.split(" ", 1)[1].rsplit(" ", 1))
            elif line.startswith("DEFINE "):
                self.variables.append(line.split(" ", 1)[1].split(" ", 1))
            elif line.startswith("SCENE_START "):
                if scene_start_found:
                    logger.log.warn("A scene start has already been defined, overriding")
                    logger.log.warn("See line {}".format(index + 1))
                scene_start_found = True

                if "GOTO " not in line:
                    raise NoStartException("START_SCENE expression on line {} is invalid: Missing GOTO".format(index + 1))

                self.start = util.parse_goto(line.split("SCENE_START ")[1])
            elif line.startswith("SCENE_END "):
                if scene_end_found:
                    logger.log.warn("A scene end has already been defined, overriding")
                    logger.log.warn("See line {}".format(index + 1))
                scene_end_found = True

        if self.title is None:
            raise MissingArgumentException("Missing SCENE tag (No scene title)")
        if self.subtitle is None:
            raise MissingArgumentException("Missing SCENE_SUB tag (No scene subtitle)")
        if not scene_start_found:
            raise NoStartException("No SCENE_START found.")
        if not scene_end_found:
            raise NoEndException("No SCENE_END found.")

        self.class_name = util.camel_case(self.title)

        if not util.is_valid_java_variable(self.class_name):
            raise InvalidClassNameException("Class Name {} is not valid java (Modify SCENE tag)".format(self.class_name))

    def parse_chatnodes(self):
        chatnodes = []
        current_node = ""

        for line in self.lines:
            if line.split(" ")[0] in stop_lines:
                chatnodes.append(current_node)
                current_node = ""
            current_node += line + "\n"

        # Filter chatnodes
        chatnodes = [x.lstrip("\n").rstrip("\n") for x in chatnodes if x.startswith("CHATNODE")]
        self.chatnodes = [chatnode.ChatNode(c.split("\n")) for c in chatnodes]

    """
    Convert code into a java class
    """
    def generate_code(self):
        return CLASS_TEMPLATE.format(
            classname=self.class_name,
            title=self.title,
            subtitle=self.subtitle,
            background=self.background_id,
            music_code=self.generate_music_code(),
            sound_code=self.generate_sound_code(),
            variable_code=self.generate_variable_code(),
            class_code="\n".join([c.generate_code() for c in self.chatnodes]),
            add_chatnode_code="",
            go_to_start=util.indent_code(self.start.replace("conversation.", "this."), 2)
        )

    """
    Generate the code in the constructor
    that pre-loads all sounds
    """
    def generate_sound_code(self):
        if len(self.sounds) == 0:
            return ""

        string = "\n        /* Pre-load sounds */\n"
        for sound in self.sounds:
            string += "        this.sounds.put(\"{}\", Gdx.audio.newSound(Gdx.files.internal(\"{}\")));\n" \
                .format(sound[1], sound[0])
        return string

    """
    Generate the code in the constructor
    that pre-loads all music
    """
    def generate_music_code(self):
        if len(self.musics) == 0:
            return ""

        string = "\n        /* Pre-load music */\n"
        for song in self.sounds:
            string += "        this.music.put(\"{}\", Gdx.audio.newMusic(Gdx.files.internal(\"{}\")));\n" \
                .format(song[1], song[0])
        return string

    """
    Generate the code in the constructor
    that defines local variables
    """
    def generate_variable_code(self):
        if len(self.variables) == 0:
            return ""

        string = "\n        /* Define local variables */\n"
        for var in self.variables:
            string += "        this.variables.put(\"{}\", {});\n" \
                .format(var[1], var[0])
        return string


# Exceptions
class NoStartException(Exception):
    pass


class NoEndException(Exception):
    pass


class MissingArgumentException(Exception):
    pass


class InvalidClassNameException(Exception):
    pass
