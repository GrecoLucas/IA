# Constantes do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = 8
GRID_HEIGHT = 8
BOARD_X = (SCREEN_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
BOARD_Y = 50

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (50, 50, 50)
WOOD_LIGHT = (240, 210, 155)
WOOD_MEDIUM = (210, 180, 140)
WOOD_DARK = (160, 120, 90)
GREEN_POINT = (0, 200, 0)
RED_POINT = (200, 0, 0)
WOOD_COLORS = [WOOD_LIGHT, WOOD_MEDIUM, WOOD_DARK]
BACKGROUND_COLOR = (240, 240, 240)

# Bot Optimal, se quiser melhorar a performance, diminua a profundidade máxima 
BOT_MOVE_DELAY = 200
MAX_SIMULATION_DEPTH = 10
MAX_TRIES = 500

# Bot BFA
MAX_BFA_MOVES = 100
# Bot Types
from enum import Enum
class BotType(Enum):
    RANDOM = "random"
    OPTIMAL = "optimal"
    GREEDY = "greedy"
    BFA = "bfa"

# Rules
RULES_COLOR = (10, 60, 10)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

RULES_TEXT = [
                "Modo Jogador:",
            "• Arraste e solte blocos de madeira no tabuleiro.",
            "• Para passar de fase é necessário pegar as peças ",
            "verdes ou vermelhas indicadas no canto inferior esquerdo",
            "completando a linha ou coluna.",
            "• Se não houver mais espaço no tabuleiro, o jogo acaba.",
            "• Tente chegar no ultimo nivel com o menor ",
            "numero de movimentos possíveis.",
            "Modo Bot:",
            "• Aperte a tecla 'P' para o bot fazer o movimento.",
]