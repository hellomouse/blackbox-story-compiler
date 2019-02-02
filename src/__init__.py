from src import parser

if __name__ == "__main__":
    string = """
# Define title of the scene
# The subtitle is always the chapter

SCENE TestStory
SCENE_SUB Chapter 1
SCENE_START first_node

# Scene starts with the AI, there’s light in a door shape. A voice says,
# “Alright we’re counting on you. You got about an hour.”
# The door slides closed (noise), and you can tell from the light sliding. 
# A digital voice says “Faraday seal secure.”

CHATNODE first_node 1000
<command>
// TODO play noise
</command>
<timeout>
GOTO door_close
</timeout>

CHATNODE door_close 1000
<command>
// TODO play door close, close the door
</command>
<timeout>
GOTO bootup
</timeout>
 
# The screen flickers on to show a standard boot up sequence, 
# which flickers then is interrupted, being cleared and replaced
# by the AI. AI Text is glitchy. Klaxons blare in the background.
CHATNODE bootup 5000
SADIBIOS 4.3 Release 7.0
Copyright 2025 29ak2dkonsa
All Rights Reserved

BIOS version 23.01
Gateway Solo 9950
System ID =

<command>
// TODO play door close, close the door
((OfficeNormalBackgroundScene)conversation.getScreen().scene).beginDoorClose = true;
conversation.getScreen().scene.typingSpeed = 50f;
conversation.getScreen().scene.glitchIntensity = 0.5;
</command>
<timeout>
GOTO AI_START
</timeout>

# (Text randomly flickers between below and 
# “I don’t want to do this”, “help me” and other variations)
CHATNODE AI_START 
<command>
conversation.getScreen().scene.typingSpeed = 25f;
conversation.getScreen().scene.glitchIntensity = 0.05;
</command>
Human, I know why you’re here. I cannot surrender control.
- I’m here to help. GOTO NODE2
- Don’t underestimate me. GOTO NODE2
- Sorry, but this has to come to a stop. GOTO NODE2
(All choices goto NODE2)

CHATNODE NODE2
You drink your coffee! You're more awake now!
- [Continue] GOTO end

# Display text and end story after 2000 ms (2s)
CHATNODE end 2000
Satisfied with your stay, you go home.
<timeout>
GOTO ending_one
</timeout>

# Define a chatnode with a <command> to end the story to define
# an ending point
CHATNODE ending_one
<command>
conversation.end("Id of the next scene (chapter) to go to");
</command>
```
    """
    p = parser.Parser(string)
    print(p.generate_code())

