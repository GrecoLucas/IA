from datetime import datetime
from model.block import Block
from model.level import Level
from shapes import SHAPES
from levels import LEVEL_MAP, LEVELS
from constants import *

class Game:
    def __init__(self):
        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        block_panel_height = 210
        block_width = GRID_SIZE * 4  
        spacing = (SCREEN_WIDTH - (3 * block_width)) // 4  
        
        self.block_positions = [
            (spacing, SCREEN_HEIGHT - block_panel_height),
            (spacing * 2 + block_width, SCREEN_HEIGHT - block_panel_height),
            (spacing * 3 + block_width * 2, SCREEN_HEIGHT - block_panel_height)
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
        self.available_blocks = [None, None, None]
        self.number_of_moves = 0
        self.total_moves = 0
        self.player_type = None
        self.bot_type = None
        self.message_log = []
        self.max_messages = 5  
        self.is_fully_automatic = False
        self.starttime = datetime.now()
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
                difficulty= getattr(level_data, 'difficulty', 1),
                sequence=level_data.sequence,
                name=getattr(level_data, 'name', None)
            )

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
            print("No sequence defined, using random blocks")
            return [Block() for _ in range(3)]  # 3 random blocks
        
        blocks = [None, None, None]  # Initialize with three positions
        
        # Get next 3 blocks from sequence
        for i in range(3):
            shape_name = self.current_level.get_next_block_name()
       
            # Check if block name exists in SHAPES
            if shape_name and shape_name in SHAPES:
                blocks[i] = Block(shape_name)
            else:
                if shape_name:
                    print(f"ERROR: Shape '{shape_name}' not found in SHAPES!")
                # Use a random block if name doesn't exist
                blocks[i] = Block()

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
        
        # Increment the move counter when a block is placed
        self.number_of_moves += 1
        self.total_moves += 1
        
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
        
        rows_cleared, cols_cleared = self.clear_rows_and_cols()
        
        return rows_cleared > 0 or cols_cleared > 0

    def clear_rows_and_cols(self):
        rows_to_clear = []
        cols_to_clear = []
        
        # Identify rows to clear
        for y in range(GRID_HEIGHT):
            if all(self.board[y][x] is not None for x in range(GRID_WIDTH)):
                rows_to_clear.append(y)
        
        # Identify columns to clear
        for x in range(GRID_WIDTH):
            if all(self.board[y][x] is not None for y in range(GRID_HEIGHT)):
                cols_to_clear.append(x)
        
        # Create a set of cells to clear (avoiding duplicates at intersections)
        cells_to_clear = set()
        
        # Add all cells from rows that need clearing
        for y in rows_to_clear:
            for x in range(GRID_WIDTH):
                cells_to_clear.add((x, y))
        
        # Add all cells from columns that need clearing
        for x in cols_to_clear:
            for y in range(GRID_HEIGHT):
                cells_to_clear.add((x, y))
        
        # Clear cells and collect stones
        for x, y in cells_to_clear:
            if self.board_types[y][x] == 2:  
                self.green_stones_collected += 1
            elif self.board_types[y][x] == 3: 
                self.red_stones_collected += 1
            
            self.board[y][x] = None
            self.board_types[y][x] = 0
        
        return len(rows_to_clear), len(cols_to_clear)
    
    def check_game_over(self):
        # Check if any available block can be placed on the board
        can_place_any = False
        for block in self.available_blocks:
            if not block:  # Skip if block was used
                continue
                
            can_place = False
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.is_valid_position(block, x, y):
                        can_place = True
                        can_place_any = True
                        break
                if can_place:
                    break
        
        # If no blocks can be placed, game is over
        return not can_place_any
    
    def all_blocks_used(self):
        # Check if all available blocks have been used
        return all(block is None for block in self.available_blocks)
        
    def check_level_complete(self):
        # Level is complete if all required stones are collected
        return (self.green_stones_collected >= self.green_stones_to_collect and 
                self.red_stones_collected >= self.red_stones_to_collect)
    
    def get_next_level(self):
        next_levels = [level.level_num for level in LEVELS if level.level_num > self.level_num]
        if next_levels:
            return min(next_levels)
        return None
    
    def save_game_stats(self):
        import csv
        import os
        from datetime import datetime
        
        # Nome do arquivo de histórico
        csv_filename = "game_history.csv"
        file_exists = os.path.isfile(csv_filename)
        
        # Data e hora atual
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Initialize starttime if it doesn't exist
        if not hasattr(self, 'starttime'):
            self.starttime = datetime.now()
        
        # Calculate elapsed time
        elapsed_time = datetime.now() - self.starttime
        elapsed_seconds = int(elapsed_time.total_seconds())
        
        # Format elapsed time as HH:MM:SS
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_spent = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Determine player type and bot type for logging
        player_type_str = "HUMAN" if self.player_type is None else "BOT"
        bot_type_str = "NONE" if self.bot_type is None else str(self.bot_type)
        
        
        # Dados para salvar
        data = {
            'timestamp': current_time,
            'time_spent': time_spent,
            'player_type': player_type_str,
            'bot_type': bot_type_str,
            'level': self.level_num,
            'moves': self.number_of_moves,
            'green_collected': self.green_stones_collected,
            'red_collected': self.red_stones_collected,
            'total_moves': self.total_moves,
            'level_complete': self.check_level_complete(),
            'game_over': self.game_over,
            'game_won': self.game_won,
            'Is_fully_automatic': self.is_fully_automatic
        }
        
        # Campos do CSV
        fieldnames = [
            'timestamp', 'time_spent', 'player_type', 'bot_type', 'level', 'moves', 
            'green_collected', 'red_collected', 'total_moves', 
            'level_complete', 'game_over', 'game_won', 'Is_fully_automatic'
        ]
        
        try:
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escrever cabeçalho apenas se o arquivo for novo
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(data)
                print(f"Game stats saved to {csv_filename}: {player_type_str} - {bot_type_str}, Time: {time_spent}")
                
        except Exception as e:
            print(f"Error saving game stats: {e}")

    def set_player_type(self, player_type):
        self.player_type = player_type

    
    def reset_from_level0(self):
        self.__init__()
        
    def reset(self):
        # Store the current level number before reset
        current_level_num = self.level_num
        
        # Store the total moves (we want to preserve this)
        #total_moves_before_reset = self.total_moves
        
        # Clear the message log
        self.message_log = []
        
        # Reload the current level
        self.load_level(current_level_num)
        
        # Restore the total moves count (since load_level resets it)
        self.total_moves = 0#total_moves_before_reset
        
        # Reset game state flags
        self.game_over = False
        self.game_won = False
        
        # Clear selection
        self.selected_block = None

    def set_bot_type(self, bot_type):
        self.bot_type = bot_type

    def make_move(self, block_index, x, y):
        block = self.available_blocks[block_index]
        if self.is_valid_position(block, x, y):
            self.place_block(block, x, y)
            self.available_blocks[block_index] = None
            return True
        return False

    def add_message(self, message):
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)

    def set_fully_automatic(self, value):
        if value:
            self.is_fully_automatic = True
    