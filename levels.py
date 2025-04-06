from level_parser import parse_levels_file
import os

class LevelData:
    def __init__(self, level_num, green_goal, red_goal, sequence, grid, difficulty = 0, name=None):
        self.level_num = level_num  # Número do nível
        self.green_goal = green_goal  # Pedras verdes a coletar
        self.red_goal = red_goal  # Pedras vermelhas a coletar
        self.sequence = sequence  # Block sequence, repeated if sequence ends, leave empty for random
        self.grid = grid  # Board layout
        self.difficulty = difficulty # Level difficulty
        self.name = name or f"Level {level_num}"  # Name of the level

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
    (level.level_num, level.green_goal, level.red_goal, level.sequence, level.grid, level.difficulty)
    for level in LEVELS
]