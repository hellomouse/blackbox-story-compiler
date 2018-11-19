from src import parser

if __name__ == "__main__":
    string = """
    SCENE test scene
    SCENE_SUB test
    SCENE_START test
    SCENE_END test
    
    SOUND dir/test asda/asd id
    
    MUSIC dir/test isad
    
    DEFINE var id
    """
    p = parser.Parser(string)
    print(p.generate_code())