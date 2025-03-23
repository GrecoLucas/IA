import pygame
from constants import *
from view.block_view import BlockView

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
    
    def render(self, game):
        self.draw_background()
        self.draw_title(game)
        self.draw_board(game)
        self.draw_available_blocks(game)
        if game.selected_block:
            self.draw_selected_block(game)
            
        self.draw_objectives(game)
        
        if game.game_over:
            self.draw_game_over()
        elif game.game_won:
            self.draw_game_won()
    
    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
    
    def draw_title(self, game):
        title_text = f"Wood Block Puzzle - Nível {game.level_num}"
        if game.current_level and game.current_level.name:
            title_text = f"Wood Block Puzzle - {game.current_level.name}"
            
        title = self.title_font.render(title_text, True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
    
    def draw_board(self, game):
        # Draw board background
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, WOOD_DARK, board_rect, 2)

        # Draw grid lines
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen, GRID_COLOR, 
                (BOARD_X + i * GRID_SIZE, BOARD_Y), 
                (BOARD_X + i * GRID_SIZE, BOARD_Y + GRID_HEIGHT * GRID_SIZE),
                1
            )
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen, GRID_COLOR, 
                (BOARD_X, BOARD_Y + i * GRID_SIZE), 
                (BOARD_X + GRID_WIDTH * GRID_SIZE, BOARD_Y + i * GRID_SIZE),
                1
            )

        # Draw blocks placed on the board
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if game.board[y][x]:
                    color = game.board[y][x]
                    rect = pygame.Rect(
                        BOARD_X + x * GRID_SIZE, 
                        BOARD_Y + y * GRID_SIZE, 
                        GRID_SIZE, GRID_SIZE
                    )
                    
                    # Add special border for gems
                    if color == GREEN_POINT:
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (0, 150, 0), rect, 2)
                    elif color == RED_POINT:
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (150, 0, 0), rect, 2)
                    else:
                        # Use BlockView for wood blocks
                        BlockView.draw_wood_block(self.screen, color, rect)
    
    def draw_available_blocks(self, game):
        # Draw all three available blocks
        for i in range(3):
            if game.available_blocks[i]:  
                block = game.available_blocks[i]
                # Get position from block_positions
                block_x, block_y = game.block_positions[i]
                
                # Draw the block
                BlockView.draw_available_block(self.screen, block, (block_x, block_y), self.font)
    
    def draw_selected_block(self, game):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x - BOARD_X) // GRID_SIZE
        grid_y = (mouse_y - BOARD_Y) // GRID_SIZE
        
        # Adjust for block offset
        grid_x -= game.selected_block.offset_x
        grid_y -= game.selected_block.offset_y
        
        # Check if position is valid
        valid_position = game.is_valid_position(game.selected_block, grid_x, grid_y)
        
        # Draw the block at mouse position
        BlockView.draw_block(self.screen, game.selected_block, grid_x, grid_y, valid_position)
    
    def draw_objectives(self, game):
        pygame.draw.rect(self.screen, GREEN_POINT, (20, SCREEN_HEIGHT - 80, 30, 30))
        objective_text = self.font.render(
            f": {game.green_stones_collected}/{game.green_stones_to_collect}",
            True, WOOD_DARK
        )
        self.screen.blit(objective_text, (55, SCREEN_HEIGHT - 76))
        
        pygame.draw.rect(self.screen, RED_POINT, (20, SCREEN_HEIGHT - 40, 30, 30))
        objective_text = self.font.render(
            f": {game.red_stones_collected}/{game.red_stones_to_collect}",
            True, WOOD_DARK
        )
        self.screen.blit(objective_text, (55, SCREEN_HEIGHT - 36))
        
        moves_text = self.font.render(
            f"Movimentos: {game.number_of_moves}", 
            True, WOOD_DARK
        )
        self.screen.blit(moves_text, (400, SCREEN_HEIGHT - 30))

        total_moves_text = self.font.render(
            f"Total de movimentos: {game.total_moves}", 
            True, WOOD_DARK
        )
        self.screen.blit(total_moves_text, (399, SCREEN_HEIGHT - 50))
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        gameover_text = self.title_font.render("GAME OVER", True, WHITE)
        restart_text = self.font.render("Pressione R para reiniciar", True, WHITE)
        
        self.screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    def draw_game_won(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.title_font.render("PARABÉNS! VOCÊ VENCEU!", True, WHITE)
        restart_text = self.font.render("Pressione R para jogar novamente", True, WHITE)
        
        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))