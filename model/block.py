import random
from shapes import SHAPES
from constants import *

class Block:
    def __init__(self, shape_name=None):
        if shape_name and shape_name in SHAPES:
            # Usar um formato específico quando fornecido
            self.shape_name = shape_name
            self.shape = SHAPES[shape_name]
        else:
            self.shape_name = random.choice(list(SHAPES.keys()))
            self.shape = SHAPES[self.shape_name]
            
        self.color = random.choice(WOOD_COLORS)
        self.rows = len(self.shape)
        self.cols = max(len(row) for row in self.shape)  # Encontra o comprimento máximo das linhas
        self.x = random.randint(0, GRID_WIDTH - self.cols)
        self.y = 0
        self.selected = False
        self.offset_x = 0
        self.offset_y = 0
    
    def get_cells(self):
        """Retorna as células ocupadas pelo bloco"""
        cells = []
        for row in range(self.rows):
            for col in range(len(self.shape[row])):
                if col < len(self.shape[row]) and self.shape[row][col] == "X":
                    cells.append((col, row))
        return cells