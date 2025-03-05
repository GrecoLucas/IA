import pygame
from constants import *

class BlockView:
    @staticmethod
    def draw_wood_block(screen, color, rect):
        """Draw a wood-textured block at the specified rectangle"""
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (color[0] - 20, color[1] - 20, color[2] - 20), rect, 1)
        
        # Add wood texture lines
        for line in range(1, 3):
            y_pos = rect.top + line * rect.height // 3
            pygame.draw.line(
                screen, 
                (color[0] - 10, color[1] - 10, color[2] - 10),
                (rect.left, y_pos),
                (rect.right, y_pos),
                1
            )
    
    @staticmethod
    def draw_block(screen, block, grid_x, grid_y, valid_position=True):
        """Draw a block at grid position with validity check"""
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if col < len(block.shape[row]) and block.shape[row][col] == "X":
                    rect = pygame.Rect(
                        BOARD_X + (grid_x + col) * GRID_SIZE,
                        BOARD_Y + (grid_y + row) * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    
                    # Use red for invalid positions, otherwise the block's color
                    color = block.color if valid_position else (255, 100, 100)
                    
                    BlockView.draw_wood_block(screen, color, rect)

    @staticmethod
    def draw_available_block(screen, block, position, font):
        """Draw a block in the selection area at the bottom of the screen"""
        x, y = position
        
        # Draw selection background
        selection_rect = pygame.Rect(
            x - 10, 
            y - 10,
            block.cols * GRID_SIZE + 20,
            block.rows * GRID_SIZE + 20
        )
        pygame.draw.rect(screen, (240, 240, 240), selection_rect, border_radius=10)
        pygame.draw.rect(screen, WOOD_DARK, selection_rect, 2, border_radius=10)
        
        # Draw the block
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if col < len(block.shape[row]) and block.shape[row][col] == "X":
                    rect = pygame.Rect(
                        x + col * GRID_SIZE,
                        y + row * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    BlockView.draw_wood_block(screen, block.color, rect)
        
        # Draw block name
        if font:
            block_name_text = font.render(f"{block.shape_name}", True, WOOD_DARK)
            screen.blit(block_name_text, 
                (x + (block.cols * GRID_SIZE) // 2 - block_name_text.get_width() // 2, 
                y + block.rows * GRID_SIZE + 10))