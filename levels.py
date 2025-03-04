# Niveis que serão usados no jogo
# 0 espaço vazio
# 1 blocos normais (madeira)
# 2 blocos verdes (objetivos a coletar)
# 3 blocos vermelhos (pontos extras)

class LevelData:
    def __init__(self, level_num, green_goal, red_goal, sequence, grid, name=None):
        self.level_num = level_num  # Número do nível
        self.green_goal = green_goal  # Pedras verdes a coletar
        self.red_goal = red_goal  # Pedras vermelhas a coletar
        self.sequence = sequence  # Sequência de blocos
        self.grid = grid  # Layout do tabuleiro
        self.name = name or f"Nível {level_num}"  # Nome descritivo do nível

# Definição de níveis como objetos LevelData
LEVELS = [
    LevelData(
        level_num=0,
        green_goal=2,
        red_goal=0,
        name="Tutorial",
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
        ]
    ),
    
    LevelData(
        level_num=1,
        green_goal=5,
        red_goal=0,
        name="Fortificação",
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
        ]
    ),
    
    LevelData(
        level_num=2,
        green_goal=3,
        red_goal=3,
        name="Canto e Centro",
        sequence=["O", "Z", "|-", "right_up_corner", "single", "single", 
                 "L", "J", "L", "J", "I", "T_INVERTIDO"],
        grid=[
            [2, 2, 2, 0, 0, 1, 1, 1],
            [2, 0, 0, 0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 3],
            [1, 1, 1, 0, 0, 3, 3, 3]
        ]
    ),
    
    LevelData(
        level_num=3,
        green_goal=5,
        red_goal=2,
        name="Espelho",
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
        ]
    )
]

# Dicionário para acesso rápido por número de nível
LEVEL_MAP = {level.level_num: level for level in LEVELS}

# Para manter compatibilidade com o código existente que espera a estrutura de tupla
# Se você não puder modificar outros arquivos, mantenha isso:
LEVEL = [
    (level.level_num, level.green_goal, level.red_goal, level.sequence, level.grid)
    for level in LEVELS
]