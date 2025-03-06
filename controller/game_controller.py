import pygame
from constants import BOARD_X, BOARD_Y, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class GameController:
    def __init__(self, game, view):
        self.game = game
        self.view = view
        self.dragging = False
        self.animation_delay = 100  # ms
    
    def handle_event(self, event):
        # Handle restart with R key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (self.game.game_over or self.game.game_won):
                self.game.reset()        
        # Skip other events if game is over
        if self.game.game_over or self.game.game_won:
            return
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.handle_mouse_down(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:  # Left mouse button release
                self.handle_mouse_up(event.pos)
    
    def handle_mouse_down(self, pos):
        mouse_x, mouse_y = pos
        
        # Check if clicked on available block
        if self.game.available_blocks[0]:
            block = self.game.available_blocks[0]
            block_pos = self.game.block_positions[0]
            
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
                    self.dragging = True
    
    def handle_mouse_up(self, pos):
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
                self.game.available_blocks[0] = None  # Mark block as used
                # Visual effect when clearing rows/columns
                if animation_needed:
                    self.view.render(self.game)
                    pygame.display.flip()
                    pygame.time.delay(self.animation_delay)
                # Check if level is complete
                if self.game.check_level_complete():
                    next_level = self.game.get_next_level()
                    if next_level is not None:
                        self.game.load_level(next_level)
                    else:
                        self.game.game_won = True
                        # Salvar estatísticas quando o jogo for ganho
                        self.game.save_game_stats()
                # Generate new blocks if needed
                elif self.game.available_blocks[0] is None:
                    self.game.available_blocks = self.game.get_next_blocks_from_sequence()
        self.game.selected_block = None

    def update(self):
        # Check game over condition
        if not self.game.game_over and not self.game.game_won:
            if self.game.check_game_over():
                self.game.game_over = True
                self.game.save_game_stats()
