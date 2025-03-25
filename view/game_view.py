import pygame
from constants import *
from view.block_view import BlockView
from model.bot import Bot
import copy

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.help_active = False  # Track if help is being displayed
        self.hint_active = False  # Track if a hint is being displayed
        self.hint_block = None    # Block suggested by the bot
        self.hint_x = None        # X position for the hint
        self.hint_y = None        # Y position for the hint
    
    def render(self, game):
        self.draw_background()
        self.draw_title(game)
        self.draw_board(game)
        self.draw_available_blocks(game)
        if game.selected_block:
            self.draw_selected_block(game)
            
        if self.hint_active and self.hint_block:
            self.draw_hint(game)
            
        self.draw_objectives(game)
        self.draw_bot_messages(self.screen, game)  

        if game.bot_type is None:
            self.draw_help_button()

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
        board_x = BOARD_X

        if hasattr(game, 'bot_type') and game.bot_type:
            if game.bot_type == BotType.BFA:
                board_x = NBOARD_X

        board_rect = pygame.Rect(board_x, BOARD_Y, GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, WOOD_DARK, board_rect, 2)

        # Draw grid lines
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen, GRID_COLOR, 
                (board_x + i * GRID_SIZE, BOARD_Y), 
                (board_x + i * GRID_SIZE, BOARD_Y + GRID_HEIGHT * GRID_SIZE),
                1
            )
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen, GRID_COLOR, 
                (board_x, BOARD_Y + i * GRID_SIZE), 
                (board_x + GRID_WIDTH * GRID_SIZE, BOARD_Y + i * GRID_SIZE),
                1
            )

        # Draw blocks placed on the board
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if game.board[y][x]:
                    color = game.board[y][x]
                    rect = pygame.Rect(
                        board_x + x * GRID_SIZE, 
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
        board_x = BOARD_X
        if hasattr(game, 'bot_type') and game.bot_type:
            if game.bot_type == BotType.BFA:
                board_x = NBOARD_X
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x - board_x) // GRID_SIZE
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
        menu_text = self.font.render("Pressione ESC para voltar ao menu", True, WHITE)
        
        self.screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
    
    def draw_game_won(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.title_font.render("PARABÉNS! VOCÊ VENCEU!", True, WHITE)
        restart_text = self.font.render("Pressione R para jogar novamente", True, WHITE)
        
        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    def draw_help_button(self):
        help_text = self.font.render("Ajuda", True, WOOD_DARK)
        help_rect = pygame.Rect(SCREEN_WIDTH - 100, 40, 80, 30)
        pygame.draw.rect(self.screen, WOOD_MEDIUM, help_rect)
        pygame.draw.rect(self.screen, WOOD_DARK, help_rect, 2)
        self.screen.blit(help_text, (SCREEN_WIDTH - 90, 45))
        
        # Only show help panel if help is active and hint is not active
        if self.help_active and not self.hint_active:
            self.draw_help_panel()
        
    def get_help_button_rect(self):
        return pygame.Rect(SCREEN_WIDTH - 100, 40, 80, 30)
    
    def get_close_help_button_rect(self):
        panel_width, panel_height = 500, 350
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        return pygame.Rect(panel_x + panel_width - 100, panel_y + panel_height - 50, 80, 30)

    def draw_bot_messages(self, screen, game):  # Add game parameter
        # Create a more compact, less obtrusive log display
        if hasattr(game, 'message_log') and game.message_log:
            # Limit to showing only the 3 most recent messages
            recent_messages = game.message_log[-3:]
            
            # Create a panel with wider width to fit longer messages
            message_panel = pygame.Rect(SCREEN_WIDTH - 430, 80, 400, 15 + 20 * len(recent_messages))
            overlay = pygame.Surface((message_panel.width, message_panel.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))  # More transparent background
            screen.blit(overlay, message_panel)
            
            # Draw a thin border
            pygame.draw.rect(screen, (100, 100, 100), message_panel, 1)
            
            # Draw the messages
            font = pygame.font.Font(None, 18)  # Smaller font
            message_y = message_panel.y + 10
            
            for message in recent_messages:
                # Adjust truncation length since we have wider panel now
                if len(message) > 60:  # Increased from 40
                    display_text = message[:57] + "..."
                else:
                    display_text = message
                    
                text_surface = font.render(display_text, True, (220, 220, 220))
                screen.blit(text_surface, (message_panel.x + 10, message_y))
                message_y += 20
    
    def draw_hint(self, game):
        board_x = BOARD_X
        if hasattr(game, 'bot_type') and game.bot_type:
            if game.bot_type == BotType.BFA:
                board_x = NBOARD_X
                
        for row in range(len(self.hint_block.shape)):
            for col in range(len(self.hint_block.shape[row])):
                if self.hint_block.shape[row][col] == "X":
                    hint_rect = pygame.Rect(
                        board_x + (self.hint_x + col) * GRID_SIZE, 
                        BOARD_Y + (self.hint_y + row) * GRID_SIZE, 
                        GRID_SIZE, GRID_SIZE
                    )
                    hint_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    hint_surface.fill((42, 157, 143, 160))  
                    self.screen.blit(hint_surface, hint_rect)
                    pygame.draw.rect(self.screen, (0, 128, 128), hint_rect, 2)  
    def draw_comeback_to_menu(self):
        comeback_text = self.font.render("Pressione ESC para voltar ao menu", True, WOOD_DARK)
        self.screen.blit(comeback_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30))

    def set_hint(self, block, x, y):
        self.hint_block = block
        self.hint_x = x
        self.hint_y = y
        self.hint_active = True
        self.help_active = False  
    
    def clear_hint(self):
        self.hint_active = False
        self.hint_block = None
        self.hint_x = None
        self.hint_y = None
