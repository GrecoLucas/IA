import pygame
from constants import *
from model.menu import PlayerType

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 28)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.background_image = None
        # Tente carregar uma imagem de fundo, se disponível
        try:
            self.background_image = pygame.image.load('resources/menu_background.jpg')
            self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Menu background image not found, using solid color")
    
    def draw(self, menu):
        """Desenha o menu na tela"""
        # Desenhar fundo
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
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
        for i, item in enumerate(menu.items):
            color = WOOD_DARK
            bg_color = None
            
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
            if i < 2:  # Opções de jogador
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