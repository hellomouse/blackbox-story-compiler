from src import parser

if __name__ == "__main__":
    string = """
SCENE test scene
SCENE_SUB test
SCENE_START GOTO test
SCENE_END test

SOUND dir/test asda/asd id

MUSIC dir/test isad

CHATNODE id
<command>test</command>
<choice>
testadsa
GOTO ads
</choice>

CHATNODE 1 2
there must be some text here
<choice>test 
GOTO ffs</choice>
<choice>test 1
GOTO ffs</choice>
<choice>test 2
GOTO ffs</choice>
<choice>test 3
GOTO ffs</choice>
- test adsasd      GOTO test
<timeout>
GOTO test
</timeout>

DEFINE var id
    """
    p = parser.Parser(string)
    print(p.generate_code())