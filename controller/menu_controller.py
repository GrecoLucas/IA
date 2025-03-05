import pygame
from model.menu import MenuState

class MenuController:
    def __init__(self, menu, menu_view):
        self.menu = menu
        self.menu_view = menu_view
    
    def handle_events(self):
        """Processa eventos de entrada do usuário"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu.move_selection(-1)  # Move seleção para cima
                elif event.key == pygame.K_DOWN:
                    self.menu.move_selection(1)   # Move seleção para baixo
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.menu.select_current()    # Seleciona o item atual
    
    def run_menu(self):
        """Executa o loop do menu até que uma ação encerre o menu"""
        clock = pygame.time.Clock()
        
        while self.menu.get_state() == MenuState.ACTIVE:
            dt = clock.tick(60)  # Delta time em milissegundos
            self.handle_events()
            self.menu_view.draw(self.menu, dt)
        
        return self.menu.get_state(), self.menu.get_player_type()