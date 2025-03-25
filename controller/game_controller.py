import pygame
from constants import  BOARD_X, BOARD_Y, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
import copy
from model.bot import Bot
from constants import BotType

class GameController:
    def __init__(self, game, view, bot=None):
        self.game = game
        self.view = view
        self.bot = bot
        self.dragging = False
        self.selected_block_index = -1  
        self.animation_delay = 100
        self.return_to_menu = False  # Add flag to track menu return request
    
    def handle_bot_press_play(self, event):
        print("bot playing!")
        move_made = self.bot.play()
        if move_made:
            # Render após cada movimento do bot
            self.view.render(self.game)
            pygame.display.flip()
        
    def handle_bot(self, event):
        if event is None:
            return
        
        
        if event.type == pygame.KEYDOWN:
            # ESC key to return to menu (works even when game is not over)
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu = True
                return
            # Reset if game is over and R is pressed    
            elif event.key == pygame.K_r and (self.game.game_over or self.game.game_won):
                bot_type = self.bot.get_bot().algorithm
                self.game.reset()
                self.game.set_bot_type(bot_type)
                self.bot.reset()       
            elif event.key == pygame.K_p:
                self.handle_bot_press_play(event)

    def handle_event(self, event):
        if event is None:  
            return
        
        if self.bot: 
            self.handle_bot(event)
            return  # Exit early for bot mode
            
        # Player mode event handling
        if event.type == pygame.KEYDOWN:
            # ESC key to return to menu (works even when game is not over)
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu = True
                return
            # Reset if game is over and R is pressed
            elif event.key == pygame.K_r and (self.game.game_over or self.game.game_won):
                self.game.reset()       
        
        # Skip other events if game is over
        if self.game.game_over or self.game.game_won:
            return
        
        # Handle mouse events (only for human player)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.handle_mouse_down(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:  # Left mouse button release
                self.handle_mouse_up(event.pos)
    
    def handle_mouse_down(self, pos):
        mouse_x, mouse_y = pos
        
        # Check if help button was clicked
        help_button_rect = self.view.get_help_button_rect()
        if help_button_rect.collidepoint(mouse_x, mouse_y):
            # Instead of just showing help panel, get a move suggestion
            self.get_move_suggestion()
            return
        
        # Check if close help button was clicked when help is active
        if self.view.help_active:
            close_help_button_rect = self.view.get_close_help_button_rect()
            if close_help_button_rect.collidepoint(mouse_x, mouse_y):
                self.view.help_active = False
                return
            else:
                # If help is active and click wasn't on close button, ignore other interactions
                return
        
        # Clear any active hint when clicking elsewhere
        if self.view.hint_active:
            self.view.clear_hint()
        
        # Check if clicked on any of the available blocks
        for i in range(3):
            if self.game.available_blocks[i]:
                block = self.game.available_blocks[i]
                block_pos = self.game.block_positions[i]
                
                block_rect = pygame.Rect(
                    block_pos[0] - 10, 
                    block_pos[1] - 10,
                    block.cols * GRID_SIZE + 20,
                    block.rows * GRID_SIZE + 20
                )
                
                if block_rect.collidepoint(mouse_x, mouse_y):
                    # Calculate click offset within block
                    col_clicked = (mouse_x - block_pos[0]) // GRID_SIZE
                    row_clicked = (mouse_y - block_pos[1]) // GRID_SIZE
                    
                    # Check if clicked on a block cell
                    if (0 <= row_clicked < block.rows and 
                        0 <= col_clicked < len(block.shape[row_clicked]) and 
                        block.shape[row_clicked][col_clicked] == "X"):
                        
                        self.game.selected_block = block
                        self.game.selected_block.offset_x = col_clicked
                        self.game.selected_block.offset_y = row_clicked
                        self.selected_block_index = i
                        self.dragging = True
                        break
    
    def handle_mouse_up(self, pos):
        if not self.dragging or self.selected_block_index == -1:
            return

        self.dragging = False
        mouse_x, mouse_y = pos
        # Check if released on the board
        if (BOARD_X <= mouse_x <= BOARD_X + GRID_SIZE * GRID_WIDTH and
            BOARD_Y <= mouse_y <= BOARD_Y + GRID_SIZE * GRID_HEIGHT):
            grid_x = (mouse_x - BOARD_X) // GRID_SIZE
            grid_y = (mouse_y - BOARD_Y) // GRID_SIZE
            # Adjust for block offset
            grid_x -= self.game.selected_block.offset_x
            grid_y -= self.game.selected_block.offset_y
            # Try to place the block
            if self.game.is_valid_position(self.game.selected_block, grid_x, grid_y):
                animation_needed = self.game.place_block(self.game.selected_block, grid_x, grid_y)
                
                # Mark the selected block as used
                self.game.available_blocks[self.selected_block_index] = None
                
                # Visual effect when clearing rows/columns
                if animation_needed:
                    self.view.render(self.game)
                    pygame.display.flip()

                
                # Check if level is complete
                if self.game.check_level_complete():
                    next_level = self.game.get_next_level()
                    if (next_level is not None):
                        self.game.load_level(next_level)
                    else:
                        self.game.game_won = True
                        self.game.save_game_stats()
                # Generate new blocks only if all 3 have been used
                elif self.game.all_blocks_used():
                    self.game.available_blocks = self.game.get_next_blocks_from_sequence()
                
                # Check for game over after placing a block
                if not self.game.game_over and not self.game.game_won and self.game.check_game_over():
                    self.game.game_over = True
                    self.game.save_game_stats()
        
        self.game.selected_block = None
        self.selected_block_index = -1

    def get_move_suggestion(self):
        # Create a copy of the current game to avoid modifying the actual game state
        game_copy = copy.deepcopy(self.game)
        
        # Create a temporary optimal bot
        temp_bot = Bot(game_copy, BotType.BFA)
        
        # Get the best move without actually making it
        best_move = temp_bot.find_best_bfa()
        
        if best_move:
            block_index, x, y = best_move
            suggested_block = copy.deepcopy(self.game.available_blocks[block_index])
            
            # Set the hint in the view
            self.view.set_hint(suggested_block, x, y)
            
    
    def update(self):
        if not self.game.game_over and not self.game.game_won:
            if self.game.check_game_over():
                self.game.game_over = True
                self.game.save_game_stats()
