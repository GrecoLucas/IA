from model.block import Block
from model.level import Level
from shapes import SHAPES
from levels import LEVEL_MAP, LEVELS
from constants import *

class Game:
    def __init__(self):
        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.block_positions = [
            (SCREEN_WIDTH // 2 - GRID_SIZE * 2, SCREEN_HEIGHT - 150)
        ]
        self.selected_block = None
        self.green_stones_collected = 0
        self.red_stones_collected = 0
        self.green_stones_to_collect = 0
        self.red_stones_to_collect = 0
        self.current_level = None
        self.level_num = 0
        self.game_over = False
        self.game_won = False
        self.available_blocks = [None]
        self.number_of_moves = 0
        self.player_type = None
        self.load_level(0)
    
    def load_level(self, level_num):
        # Check if the level exists
        if level_num in LEVEL_MAP:
            level_data = LEVEL_MAP[level_num]

            # Create Level object
            self.current_level = Level(
                level_num=level_data.level_num,
                green_goal=level_data.green_goal,  
                red_goal=level_data.red_goal,      
                grid=level_data.grid,
                sequence=level_data.sequence,
                name=getattr(level_data, 'name', None)
            )

            # Reset the board
            self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

            # Load the level grid configuration
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if y < len(level_data.grid) and x < len(level_data.grid[y]):
                        cell_type = level_data.grid[y][x]
                        self.board_types[y][x] = cell_type

                        if cell_type == 1:  # Normal wood block
                            self.board[y][x] = WOOD_MEDIUM
                        elif cell_type == 2:  # Green gem (objective)
                            self.board[y][x] = GREEN_POINT
                        elif cell_type == 3:  # Red gem (extra points)
                            self.board[y][x] = RED_POINT

            # Initialize level objectives
            self.level_num = level_data.level_num
            self.green_stones_collected = 0
            self.red_stones_collected = 0
            self.green_stones_to_collect = level_data.green_goal
            self.red_stones_to_collect = level_data.red_goal
            
            # Create the first blocks from the sequence
            self.available_blocks = self.get_next_blocks_from_sequence()
            
            # Reset the move counter when loading a new level
            self.number_of_moves = 0
        else:
            # If level doesn't exist, check if we finished all levels
            max_level = max(level.level_num for level in LEVELS)
            if level_num > max_level:
                self.game_won = True
            else:
                # Try loading level 0 as fallback
                if level_num != 0:
                    print(f"Level {level_num} not found. Loading level 0.")
                    self.load_level(0)
                else:
                    print("Error: No levels defined in the game.")
                    self.game_over = True

    def get_next_blocks_from_sequence(self):
        if not self.current_level or not self.current_level.sequence:
            print("No sequence defined, using random block")
            return [Block()]  # Just one block
        
        blocks = [None]  # Initialize with one position
        
        shape_name = self.current_level.get_next_block_name()
        print(f"Next block from sequence: {shape_name}")
   
        # Check if block name exists in SHAPES
        if shape_name and shape_name in SHAPES:
            blocks[0] = Block(shape_name)
        else:
            print(f"ERROR: Shape '{shape_name}' not found in SHAPES!")
            # Use a random block if name doesn't exist
            blocks[0] = Block()

        return blocks
    
    def is_valid_position(self, block, x, y):
        if x < 0 or y < 0:
            return False
            
        for cell in block.get_cells():
            col, row = cell
            board_x, board_y = x + col, y + row
            
            # Check if inside board limits
            if board_y >= GRID_HEIGHT or board_x >= GRID_WIDTH:
                return False
            # Check if cell is already occupied
            if self.board[board_y][board_x]:
                return False
        return True
    
    def place_block(self, block, x, y):
        has_cleared = False
        
        # Increment the move counter when a block is placed
        self.number_of_moves += 1
        
        # Place block on the board
        for cell in block.get_cells():
            col, row = cell
            board_x, board_y = x + col, y + row
            
            # Check if there's a green gem at position
            if self.board_types[board_y][board_x] == 2:
                # Collected a green gem
                self.green_stones_collected += 1
            
            # Check if there's a red gem at position
            elif self.board_types[board_y][board_x] == 3:
                self.red_stones_collected += 1
            
            # Remove block type from the grid
            self.board_types[board_y][board_x] = 0
            
            # Place wood block on the board
            self.board[board_y][board_x] = block.color
        
        # Check and clear complete rows/columns
        rows_cleared = self.clear_rows()
        cols_cleared = self.clear_cols()
        
        return rows_cleared > 0 or cols_cleared > 0

    def clear_rows(self):
        rows_cleared = 0
        rows_to_clear = []
        
        # Identify rows to clear
        for y in range(GRID_HEIGHT):
            if all(self.board[y][x] is not None for x in range(GRID_WIDTH)):
                rows_to_clear.append(y)
                rows_cleared += 1
        
        # Clear rows and collect stones
        for y in rows_to_clear:
            for x in range(GRID_WIDTH):
                if self.board_types[y][x] == 2:  # If there's a green gem
                    self.green_stones_collected += 1
                elif self.board_types[y][x] == 3:  # If there's a red gem
                    self.red_stones_collected += 1
                
                self.board[y][x] = None
                self.board_types[y][x] = 0
                
        return rows_cleared
    
    def clear_cols(self):
        cols_cleared = 0
        cols_to_clear = []
        
        # Identify columns to clear
        for x in range(GRID_WIDTH):
            if all(self.board[y][x] is not None for y in range(GRID_HEIGHT)):
                cols_to_clear.append(x)
                cols_cleared += 1
        
        # Clear columns and collect stones
        for x in cols_to_clear:
            for y in range(GRID_HEIGHT):
                if self.board_types[y][x] == 2:  # If there's a green gem
                    self.green_stones_collected += 1
                elif self.board_types[y][x] == 3:  # If there's a red gem
                    self.red_stones_collected += 1
                
                self.board[y][x] = None
                self.board_types[y][x] = 0
                
        return cols_cleared
    
    def check_game_over(self):
        # Check if any available block can be placed on the board
        for block in self.available_blocks:
            if not block:  # Skip if block was used
                continue
                
            can_place = False
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.is_valid_position(block, x, y):
                        can_place = True
                        break
                if can_place:
                    break
            
            if can_place:
                return False  # At least one block can be placed
        
        # If no blocks can be placed, game is over
        return True
        
    def check_level_complete(self):
        # Level is complete if all required stones are collected
        return (self.green_stones_collected >= self.green_stones_to_collect and 
                self.red_stones_collected >= self.red_stones_to_collect)
    
    def get_next_level(self):
        next_levels = [level.level_num for level in LEVELS if level.level_num > self.level_num]
        if next_levels:
            return min(next_levels)
        return None
    
    def get_score(self):
        return self.number_of_moves
    
    def save_game_stats(self):
        import csv
        import os
        from datetime import datetime
        
        # Nome do arquivo de histórico
        csv_filename = "game_history.csv"
        file_exists = os.path.isfile(csv_filename)
        
        # Data e hora atual
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        player_type = "Bot" if self.player_type and self.player_type.name == "BOT" else "Humano"
        # Dados para salvar
        data = {
            'player_type' : player_type,
            'timestamp': current_time,
            'level': self.level_num,
            'moves': self.number_of_moves,
            'level_complete': self.check_level_complete()
        }
        
        # Campos do CSV
        fieldnames = ['player_type','timestamp', 'level', 'moves', 'level_complete']
        
        try:
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escrever cabeçalho apenas se o arquivo for novo
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(data)
                print(f"Game stats saved to {csv_filename}")
                
        except Exception as e:
            print(f"Error saving game stats: {e}")

    def set_player_type(self, type):
        self.player_type = type

    def reset(self):
        self.__init__()
