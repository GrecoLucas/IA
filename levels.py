# Niveis que serão usados no jogo
# 0 espaço vazio
# 1 blocos normais (madeira)
# 2 blocos verdes (objetivos a coletar)
# 3 blocos vermelhos (pontos extras)

from level_parser import parse_levels_file
import os

class LevelData:
    def __init__(self, level_num, green_goal, red_goal, sequence, grid, name=None):
        self.level_num = level_num  
        self.green_goal = green_goal  
        self.red_goal = red_goal 
        self.sequence = sequence  
        self.grid = grid  
        self.name = name or f"Nível {level_num}" 

# Carrega os níveis do arquivo de texto
LEVELS_FILE = "levels.txt"

if not os.path.exists(LEVELS_FILE):
    from level_parser import convert_levels_to_file
    convert_levels_to_file()

# Carrega os níveis do arquivo
LEVELS = parse_levels_file(LEVELS_FILE)

# Cria o mapa de níveis por número
LEVEL_MAP = {level.level_num: level for level in LEVELS}

# Mantém a compatibilidade com o código existente
LEVEL = [
    (level.level_num, level.green_goal, level.red_goal, level.sequence, level.grid)
    for level in LEVELS
]