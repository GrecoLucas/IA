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
            print(f"Aviso: Arquivo GIF não encontrado em {path}")
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

            print(f"Carregados {len(self.frames)} frames do GIF")
        except Exception as e:
            print(f"Erro ao carregar GIF: {e}")

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

        title = self.title_font.render("Wood Block Puzzle", True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        subtitle = self.font.render("Menu Principal", True, WOOD_DARK)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        menu_y = 200
        for i, item in enumerate(menu.items):
            color = WOOD_DARK
            if item.selected:
                select_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, menu_y - 5, 300, 40)
                pygame.draw.rect(self.screen, (240, 240, 220), select_rect, border_radius=5)
                pygame.draw.rect(self.screen, WOOD_MEDIUM, select_rect, 2, border_radius=5)

            text = self.font.render(item.text, True, color)

            if menu.state == MenuState.ACTIVE and i < 2:
                if (i == 0 and menu.get_player_type() == PlayerType.HUMAN) or \
                   (i == 1 and menu.get_player_type() == PlayerType.BOT):
                    marker = self.font.render("✓", True, (0, 150, 0))
                    self.screen.blit(marker, (SCREEN_WIDTH // 2 - 180, menu_y))

            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, menu_y))
            menu_y += 50

        instructions = self.font.render("Setas: Mover   Enter: Selecionar", True, WOOD_MEDIUM)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        if selected_bot_name:
            bot_name_text = self.font.render(f"Bot: {selected_bot_name}", True, WOOD_DARK)
            self.screen.blit(bot_name_text, (50, 50))

        pygame.display.flip()