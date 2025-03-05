import pygame
from constants import *
from view.block_view import BlockView

class LevelView:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        
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
        if game.available_blocks[0]:  
            block = game.available_blocks[0]
            # Center block at the bottom of screen
            block_x = SCREEN_WIDTH // 2 - (block.cols * GRID_SIZE) // 2
            block_y = SCREEN_HEIGHT - 200
            
            # Update block position for drawing and interaction
            game.block_positions[0] = (block_x, block_y)
            
            # Draw the block
            BlockView.draw_available_block(self.screen, block, (block_x, block_y), self.font)
    
    def draw_objectives(self, game):
        objective_text = self.font.render(
            f"Pedras verdes coletadas: {game.green_stones_collected}/{game.green_stones_to_collect}", 
            True, WOOD_DARK
        )
        self.screen.blit(objective_text, (20, SCREEN_HEIGHT - 50))
        
        objective_text = self.font.render(
            f"Pedras vermelhas coletadas: {game.red_stones_collected}/{game.red_stones_to_collect}", 
            True, WOOD_DARK
        )
        self.screen.blit(objective_text, (20, SCREEN_HEIGHT - 30))
    
    def draw_level_title(self, game):
        title_text = f"Wood Block Puzzle - Nível {game.level_num}"
        if game.current_level and game.current_level.name:
            title_text = f"Wood Block Puzzle - {game.current_level.name}"
            
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        title = title_font.render(title_text, True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
