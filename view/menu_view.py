import pygame
from constants import *
from model.menu import PlayerType, MenuState
from PIL import Image, ImageSequence
import os
import time

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 28)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 20  
        self.frames = []
        self.load_gif("resources/menu.gif")  

    def load_gif(self, path):
        """Carrega o GIF e redimensiona cada frame para o tamanho da tela."""
        if not os.path.exists(path):
            print(f"Warning: GIF file not found in {path}")
            return

        try:
            img = Image.open(path)
            self.frames = []

            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA")
                pygame_image = pygame.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode
                ).convert_alpha()

                pygame_image = pygame.transform.scale(pygame_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.frames.append(pygame_image)

            print(f"Loaded {len(self.frames)} frames from GIF")
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def update_animation(self, dt):
        """Atualiza a animação do GIF."""
        if not self.frames:
            return

        self.frame_time += dt
        if self.frame_time > self.frame_duration:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, menu, dt, selected_bot_name=None):
        """Desenha o menu na tela."""

        self.update_animation(dt)
        if self.frames and self.current_frame < len(self.frames):
            self.screen.blit(self.frames[self.current_frame], (0, 0))  

        if menu.state == MenuState.RULES:
            self.draw_rules()
        else:
            self.draw_menu_items(menu, selected_bot_name)

        pygame.display.flip()
        
    def draw_menu_items(self, menu, selected_bot_name=None):
        """Draw the main menu items"""
        title = self.title_font.render("Wood Block Puzzle", True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        subtitle = self.font.render("Menu", True, WOOD_DARK)
        if menu.state == MenuState.CHOOSE_LEVEL:
            subtitle = self.font.render("Select Level", True, WOOD_DARK)
        elif menu.state == MenuState.CHOOSE_ALGORITHM:
            subtitle = self.font.render("Select Algorithm", True, WOOD_DARK)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        visible_items = 8  
        scroll_offset = 0
        
        if menu.state == MenuState.CHOOSE_LEVEL and len(menu.items) > visible_items:
            # Calculate scroll offset based on selected index
            scroll_offset = max(0, min(menu.selected_index - 2, len(menu.items) - visible_items))
        
        # Display visible menu items
        menu_y = 200
        visible_count = min(visible_items, len(menu.items))
        
        for i in range(scroll_offset, scroll_offset + visible_count):
            if i >= len(menu.items):
                break
                
            item = menu.items[i]
            color = WOOD_DARK
            
            if item.selected:
                select_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, menu_y - 5, 400, 40)
                pygame.draw.rect(self.screen, (240, 240, 220), select_rect, border_radius=5)
                pygame.draw.rect(self.screen, WOOD_MEDIUM, select_rect, 2, border_radius=5)

            text = self.font.render(item.text, True, color)

            if menu.state == MenuState.ACTIVE and i < 7:
                if (i == 0 and menu.get_player_type() == PlayerType.HUMAN) or \
                   (i == 1 and menu.get_player_type() == PlayerType.BOT)or \
                   (i == 6 and menu.get_player_type() == PlayerType.TEST):
                    marker = self.font.render("✓", True, (0, 150, 0))
                    self.screen.blit(marker, (SCREEN_WIDTH // 2 - 180, menu_y))

            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, menu_y))
            menu_y += 50

        # Show scroll indicators if needed
        if menu.state == MenuState.CHOOSE_LEVEL and len(menu.items) > visible_items:
            if scroll_offset > 0:
                up_arrow = self.font.render("▲ More levels", True, WOOD_MEDIUM)
                self.screen.blit(up_arrow, (SCREEN_WIDTH // 2 - up_arrow.get_width() // 2, 165))
            
            if scroll_offset + visible_count < len(menu.items):
                down_arrow = self.font.render("▼ More levels", True, WOOD_MEDIUM)
                self.screen.blit(down_arrow, (SCREEN_WIDTH // 2 - down_arrow.get_width() // 2, menu_y))

        # Display instructions and selected info
        instructions = self.font.render("Arrows: Move   Enter: Select", True, WOOD_MEDIUM)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        if selected_bot_name:
            bot_name_text = self.font.render(f"Bot: {selected_bot_name}", True, WOOD_DARK)
            self.screen.blit(bot_name_text, (50, 50))
            
        # Display selected level if any
        if menu.get_selected_level() > 0:
            level_text = self.font.render(f"Level: {menu.get_selected_level()}", True, WOOD_DARK)
            self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 50, 50))

    def draw_rules(self):
        """Draw the rules screen."""
        

        # Title
        title = self.title_font.render("Game Rules", True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        
        rules_texts = RULES_TEXT
        rules_background = pygame.Rect(30, 80, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 200)
        pygame.draw.rect(self.screen, (255, 255, 240), rules_background, border_radius=10)
        pygame.draw.rect(self.screen, WOOD_MEDIUM, rules_background, 3, border_radius=10)

        y_position = 100
        small_font = pygame.font.SysFont('Arial', 25)  
        for rule in rules_texts:
            if "red" in rule or "green" in rule:
                parts = rule.split(" ")
                x_position = 80
                for part in parts:
                    if part == "green":
                        text = small_font.render(part, True, GREEN)  
                    elif part == "red":
                        text = small_font.render(part, True, RED)  
                    else:
                        text = small_font.render(part, True, RULES_COLOR)
                    self.screen.blit(text, (x_position, y_position))
                    x_position += text.get_width() + 5
                y_position += 35
            
            else:
                text = small_font.render(rule, True, RULES_COLOR)
                self.screen.blit(text, (80, y_position))
                y_position += 35

        # Back button - highlighted rectangle
        back_text = self.font.render("Return to Menu", True, WOOD_DARK)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, (240, 240, 220), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, WOOD_MEDIUM, back_rect, 2, border_radius=5)
        
        # Center the text on the button
        text_x = back_rect.centerx - back_text.get_width() // 2
        text_y = back_rect.centery - back_text.get_height() // 2
        self.screen.blit(back_text, (text_x, text_y))
        
        # Navigation hint
        hint = self.font.render("Click to return or press ESC", True, WOOD_MEDIUM)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))