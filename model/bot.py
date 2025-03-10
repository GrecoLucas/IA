from model.block import Block
from model.level import Level
from shapes import SHAPES
from levels import LEVEL_MAP, LEVELS
from constants import *
import time  # Import time module for delay
import copy

class Bot:
    def __init__(self, game):
        self.game = game
        self.last_move_time = 0
        self.move_delay = 1  # Delay in seconds between moves
        self.selected_block_index = None
        self.target_position = None
        self.state = "planning"  # States: planning, selecting, placing, waiting

    def find_best_move(self):
        possible_moves = []

        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        
        # Selecionar um movimento aleatório da lista de possíveis
        if possible_moves:
            import random
            return random.choice(possible_moves)
        return None
        
    
    def play(self):
        current_time = time.time()
        move_made = False
        
        # State machine to visualize bot's moves
        if self.state == "planning":
            # Finding the best move
            best_move = self.find_best_move()
            if best_move:
                self.selected_block_index, self.target_x, self.target_y = best_move
                self.state = "selecting"
                self.last_move_time = current_time
                move_made = True  # Visual update needed when selecting block
            else:
                # No valid moves
                self.game.game_over = True
                return True
                    
        elif self.state == "selecting" and current_time - self.last_move_time >= 0.5:
            # Visualize block selection
            self.game.selected_block = self.game.available_blocks[self.selected_block_index]
            self.state = "placing"
            self.last_move_time = current_time
            move_made = True  # Visual update needed when showing selected block
                
        elif self.state == "placing" and current_time - self.last_move_time >= 0.5:
            # Place the block
            block = self.game.available_blocks[self.selected_block_index]
            if self.game.make_move(self.selected_block_index, self.target_x, self.target_y):
                # Reset selection
                self.game.selected_block = None
                
                # Check if level complete
                if self.game.check_level_complete():
                    next_level = self.game.get_next_level()
                    if next_level is not None:
                        self.game.load_level(next_level)
                    else:
                        self.game.game_won = True
                elif self.game.all_blocks_used():
                    # Get new blocks if all used
                    self.game.available_blocks = self.game.get_next_blocks_from_sequence()
                
                # Wait before next move
                self.state = "waiting"
                self.last_move_time = current_time
                move_made = True  # Visual update needed after placing block
            else:
                # Something went wrong with the move
                self.state = "planning"
                    
        elif self.state == "waiting" and current_time - self.last_move_time >= 0.5:
            # Reset for next move
            self.state = "planning"
            move_made = True  # Visual update needed when resetting
            
        return move_made  # Return whether a visual update is needed