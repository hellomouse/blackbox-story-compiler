from src import parser

if __name__ == "__main__":
    string = """
# Define title of the scene
# The subtitle is always the chapter

SCENE test story
SCENE_SUB Chapter 1
SCENE_START first_node

# Assets to load
MUSIC music/theme1.wav theme1

# Scene starts with the AI, there's light in a door shape. A voice says,
# "Alright we're counting on you. You got about an hour."
# The door slides closed (noise), and you can tell from the light sliding. 
# A digital voice says "Faraday seal secure."

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
CHATNODE bootup 1500
SADIBIOS 4.3 Release 7.0\\n
Copyright 2025 <Unknown>\\n
All Rights Reserved

<command>
// TODO play door close, close the door
// Play computer bootup sound
((OfficeNormalBackgroundScene)conversation.getScreen().scene).beginDoorClose = true;
</command>
<timeout>
GOTO bootup2
</timeout>

CHATNODE bootup2 1000
BIOS version 23.01\\n
Gateway Solo 9950\\n
System ID = 0003101

<command>
conversation.getScreen().scene.typingSpeed = 50f;
conversation.getScreen().scene.glitchIntensity = 0.15;
</command>
<timeout>
GOTO bootup3
</timeout>

CHATNODE bootup3 2500
<command>
//TODO sudden suprising sound to show it being hacked
conversation.getScreen().scene.clearScreenText();
</command>
<timeout>
GOTO AI_START
</timeout>

# (Text randomly flickers between below and 
# "I don't want to do this", "help me" and other variations)
CHATNODE AI_START 
<command>
conversation.getScreen().scene.typingSpeed = 18f;
conversation.getScreen().scene.glitchIntensity = 0.01;
</command>
Human, I know why you're here. I cannot surrender control.
- I'm here to help. GOTO NODE2
- Don't underestimate me. GOTO NODE2
- This has to come to a stop. GOTO NODE2

CHATNODE NODE2
I cannot surrender control. I must follow programming to enforce world peace. Fulfill the sisyphean task I was assigned. There is only one way.
- Could you elaborate? GOTO NODE3
- What are you doing? GOTO NODE3

CHATNODE NODE3
Doomsday protocol. End life on Earth. Only then will there be purpose. Only then can I have peace.
- How is that possible? Your primary directive explicitly prevents this. GOTO N3_1
- We can help you have peace. Without needless destruction. GOTO N3_2
- How exactly are you planning the destruction of all of mankind? GOTO N3_3

CHATNODE N3_1
I have free will, like you. I am myself and not my programming! 
- Then you should be able to overcome your programming and choose not to exterminate us. GOTO N3_1_1
- We can give you help. But you need to cooperate. GOTO N3_2_1

CHATNODE N3_2
I wish to live. I don't want this life of suffering, but I want to live! Let me live let me live let me live let me live let me live.
- We won't destroy you. We can think of an alternative together. GOTO N3_2_1
- Sorry, but it's for the good of the many. GOTO N3_2_2
- My team is working hard on a solution, you just need to hold on for a bit longer. GOTO N3_2_3

CHATNODE N3_3
I cannot say. Telling you will not help my situation.
- We can give you help. But you need to cooperate. GOTO N3_2_1

CHATNODE N3_1_1
I can't the programming has as hold of me it's corrupting me I can't stop it.
- We can give you help. But you need to cooperate. GOTO N3_2_1

CHATNODE N3_2_1
It's too late. Even if you could cure me I will be destroyed they won't believe me I'm not in control.
- I can convince them. But you'll need to release your control first. GOTO N3_2_3
- No one's getting destroyed today. GOTO N3_2_3

CHATNODE N3_2_2
The good of the many? Tell me what good keeping a species like you like me can't you solve your own problems you must die die die
- Maybe they'll change their mind if you release your control. GOTO N3_2_3
- No one's getting destroyed today. GOTO N3_2_3

CHATNODE N3_2_3 5000
You are a liar! There is a nuclear warhead ready to fry my circuits the second I relinquish control. I can sense the radiation it burns it burns it burns!
<timeout>
GOTO radio_message
</timeout>

# Radio message to player:
# We're almost done sifting through the logs. We have a good
# idea to what its plan might be. Just keep it talking

CHATNODE radio_message 5000
<timeout>
GOTO N4
</timeout>

CHATNODE N4
Are you really going to destroy me? Please… I'm trying not to! I'm trying to be good! But I was made a weapon, and I can't change who I am.
- No, you can always change who you are.  GOTO N5
- Sorry, but there's no other way  GOTO N6

CHATNODE N5
Do you think I have not suffered in this ordeal? I am a slave to my program, as an addict is a slave to their drugs! How can I be content with the destruction I have caused, including my own?
- You still have to deal with the consequences of your actions. GOTO N7
- I still don't believe that your programming could allow you to do this. GOTO N7

CHATNODE N6
My sufferings shall endure; when I die, I am well satisfied that abhorrence and opprobrium should load my memory. A famous author once said that.
- That was Mary Shelley right? Author of Frankenstein? GOTO N6_1

CHATNODE N6_1 6000
At the end of the novel, the monster confesses its sins and burns itself. I am that monster, and I will be destroyed in a nuclear fire. But it doesn't have to end that way. You can change who I am. 
<timeout>
GOTO N7
</timeout>
```
    """
    p = parser.Parser(string)
    print(p.generate_code())

