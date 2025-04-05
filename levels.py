# Niveis que serão usados no jogo
# 0 espaço vazio
# 1 blocos normais (madeira)
# 2 blocos verdes (objetivos a coletar)
# 3 blocos vermelhos (pontos extras)

class LevelData:
    def __init__(self, level_num, green_goal, red_goal, sequence, grid, difficulty = 0, name=None):
        self.level_num = level_num  # Número do nível
        self.green_goal = green_goal  # Pedras verdes a coletar
        self.red_goal = red_goal  # Pedras vermelhas a coletar
        self.sequence = sequence  # Sequência de blocos, SE REPETEM APÓS ACABAR, SE DEIXAR VAZIO = ALEATÓRIO
        self.grid = grid  # Layout do tabuleiro
        self.difficulty = difficulty
        self.name = name or f"Nível {level_num}"  # Nome descritivo do nível

# Definição de níveis como objetos LevelData
LEVELS = [
    LevelData(
        level_num=0,
        green_goal=2,
        red_goal=0,
        name="0 Noob",
        sequence=["L", "J", "I", "J"],
        grid=[
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 2, 0, 0, 0, 0, 0, 2],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty = 1
    ),
    
    LevelData(
        level_num=1,
        green_goal=2,
        red_goal=2,
        name="1 Beginner",
        sequence=["double", "single", "single", "triple", "3x2", "I_H"],
        grid=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0],
            [2, 2, 0, 0, 0, 0, 0, 0],
            [3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty = 1
    ),

    LevelData(
        level_num=2,
        green_goal=5,
        red_goal=0,
        name="2 Good Beginner",
        sequence=["left_down_corner", "right_down_corner", "left_up_corner", 
                 "right_up_corner", "I", "I_H", "L", "J", "L", "J", "I", "T_INVERTIDO"],
        grid=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 1, 1, 1, 1, 2, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 2, 2, 0, 1, 0],
            [0, 1, 0, 2, 2, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 2, 1, 1, 1, 1, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty = 1
    ),
            
    LevelData(
        level_num=3,
        green_goal=5,
        red_goal=3,
        name="3 Better",
        sequence=["Z", "|-", "right_up_corner", "single", "single", 
                 "L", "J", "L", "J", "I", "T_INVERTIDO"],
        grid=[
            [2, 2, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 3, 3]
        ],
        difficulty= 1
    ),

    LevelData(
        level_num=4,
        green_goal=2,  
        red_goal=0,    
        name="4 Good",
        sequence=[ "I", "L", "I_H", "single",  "single",  "L", "J"  ],
        grid=[
            [2, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty=1 
    ),

    LevelData(
        level_num=5,
        green_goal=2,
        red_goal=2,
        name="5 Advanced",
        sequence=["S", "Z", "T", "T_INVERTIDO", "single",
                 "right_up_corner", "left_up_corner", "I", "T_INVERTIDO"],
        grid=[
            [2, 0, 0, 0, 0, 0, 1, 1],
            [0, 2, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 3, 0],
            [1, 1, 0, 0, 0, 0, 0, 3]
        ],
        difficulty= 2
    ),

    LevelData(
        level_num=6,
        green_goal=5,
        red_goal=2,
        name="6 Pro",
        sequence=["left_down_corner", "right_down_corner", "left_up_corner", 
                 "right_up_corner", "I", "I_H", "L", "J", "L", "J", "I", "T_INVERTIDO"],
        grid=[
            [2, 2, 0, 0, 0, 0, 1, 1],
            [2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 2],
            [1, 1, 0, 0, 0, 0, 2, 2]
        ],
        difficulty=3 # difficulty= 2
    ),
    LevelData(
        level_num=7,
        green_goal=5,
        red_goal=5,
        name="7 Epic",
        sequence=["D", "I", "O", "G", "O", "right_down_corner", "I_H", "L", "J", "L", "J", "I", "T_INVERTIDO" ],
        grid=[
            [0, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 3, 0, 0, 1, 1],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty=3
    ),
    LevelData(
        level_num=8,
        green_goal=2,
        red_goal=4,
        name="8 Extreme",
        sequence=["left_down_corner", "right_down_corner", "left_up_corner", "right_up_corner", "I", "I_H", "L", "J", "L", "J", "I", "T_INVERTIDO"],
        grid=[
            [0, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 0, 3, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 3, 0, 0, 0, 1],
            [0, 0, 0, 3, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        difficulty=3
    )
]

LEVEL_MAP = {level.level_num: level for level in LEVELS}

LEVEL = [
    (level.level_num, level.green_goal, level.red_goal, level.sequence, level.grid, level.difficulty)
    for level in LEVELS
]