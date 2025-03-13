import pygame
from constants import *
from model.menu import PlayerType
from PIL import Image, ImageSequence
import os
import time

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 28)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.background_frames = []
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 20

        # Carrega os frames do GIF
        self.load_gif_frames('resources/menu.gif')
    
    def load_gif_frames(self, gif_path):
        """Carrega todos os frames do GIF em uma lista de imagens Pygame"""
        try:
            # Abrir o GIF com PIL
            gif = Image.open(gif_path)
            
            # Para cada frame no GIF
            for frame_index in range(0, gif.n_frames):
                gif.seek(frame_index)  # Ir para o frame específico
                
                # Converter o frame para formato compatível com Pygame
                frame_surface = pygame.image.fromstring(
                    gif.convert('RGBA').tobytes(), gif.size, 'RGBA')
                
                # Redimensionar para tamanho da tela
                frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
                # Adicionar à lista de frames
                self.background_frames.append(frame_surface)
            
            print(f"GIF carregado com {len(self.background_frames)} frames")
            
        except Exception as e:
            print(f"Erro ao carregar GIF: {e}")
            self.background_frames = []
    
    def update_animation(self, dt):
        """Atualiza o frame atual da animação baseado no tempo decorrido"""
        if not self.background_frames:
            return
            
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.background_frames)
            self.frame_time = 0

    def draw(self, menu, dt, start_index=0, stop_index=None ):
        """Desenha o menu na tela"""
        self.update_animation(dt)
        
        # Desenhar fundo
        if self.background_frames:
            self.screen.blit(self.background_frames[self.current_frame], (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLOR)
        
        # Desenhar título
        title = self.title_font.render("Wood Block Puzzle", True, WOOD_DARK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        # Desenhar subtítulo
        subtitle = self.font.render("Menu Principal", True, WOOD_DARK)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        
        # Desenhar itens do menu
        menu_y = 200
        for i, item in enumerate(menu.items[start_index:stop_index], start=start_index):
            color = WOOD_DARK
            
            # Destacar o item selecionado
            if item.selected:
                # Desenhando retângulo de seleção
                select_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 150,
                    menu_y - 5,
                    300,
                    40
                )
                pygame.draw.rect(self.screen, (240, 240, 220), select_rect, border_radius=5)
                pygame.draw.rect(self.screen, WOOD_MEDIUM, select_rect, 2, border_radius=5)
            
            # Desenhar texto do item
            text = self.font.render(item.text, True, color)
            
            # Marcar opção ativa de tipo de jogador
            if i < 2 and start_index == 0:  # Opções de jogador
                if (i == 0 and menu.get_player_type() == PlayerType.HUMAN) or \
                   (i == 1 and menu.get_player_type() == PlayerType.BOT):
                    # Desenhar um marcador de seleção
                    marker = self.font.render("✓", True, (0, 150, 0))
                    self.screen.blit(marker, (SCREEN_WIDTH // 2 - 180, menu_y))
            
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, menu_y))
            menu_y += 50
        
        # Desenhar instruções
        instructions = self.font.render("Setas: Mover   Enter: Selecionar", True, WOOD_MEDIUM)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()