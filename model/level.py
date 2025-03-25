import random
from levels import LEVEL_MAP, LEVELS

class Level:
    def __init__(self, level_num, green_goal, red_goal, grid, sequence, name=None):
        self.level_num = level_num
        self.green_goal = green_goal        
        self.red_goal = red_goal            
        self.grid = grid
        self.sequence = sequence
        self.name = name or f"Nível {level_num}"
        self.current_block_index = 0

    def get_next_block_name(self):
        if not self.sequence:
            return None
            
        if self.current_block_index < len(self.sequence):
            block_name = self.sequence[self.current_block_index]
            self.current_block_index = (self.current_block_index + 1) % len(self.sequence)
            return block_name
        return None
    
    def is_complete(self, green_collected, red_collected):
        return (green_collected >= self.green_goal and 
                red_collected >= self.red_goal)
    
    def reset_sequence(self):
        self.current_block_index = 0
        random.shuffle(self.sequence)

    
    
