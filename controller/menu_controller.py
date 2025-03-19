import pygame
import time
from model.menu import MenuState

class MenuController:
    def __init__(self, menu_model, menu_view):
        self.menu = menu_model
        self.view = menu_view
        self.running = False
        self.last_time = time.time()
    
    def handle_events(self):
        """Processar eventos do Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu.state = MenuState.EXIT
                self.running = False
                return

            if self.menu.state == MenuState.RULES:
                self.handle_rules_events(event)
            else:
                self.handle_menu_events(event)

    def handle_menu_events(self, event):
        """Handle events for the main menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self.menu.move_selection(1)
            elif event.key == pygame.K_RETURN:
                should_exit = self.menu.select_current()
                if should_exit:
                    self.running = False
            elif event.key == pygame.K_ESCAPE:
                if self.menu.state != MenuState.ACTIVE:
                    self.menu.state = MenuState.ACTIVE
                    self.menu.initialize_menu_items()
                else:
                    self.menu.state = MenuState.EXIT
                    self.running = False
                    
    def handle_rules_events(self, event):
        """Handle events for the rules screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                # Return to main menu
                self.menu.state = MenuState.ACTIVE
                self.menu.initialize_menu_items()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if back button is clicked
            mouse_pos = pygame.mouse.get_pos()
            back_button_rect = pygame.Rect(
                pygame.display.get_surface().get_width() // 2 - 100, 
                pygame.display.get_surface().get_height() - 100, 
                200, 50
            )
            
            if back_button_rect.collidepoint(mouse_pos):
                # Return to main menu
                self.menu.state = MenuState.ACTIVE
                self.menu.initialize_menu_items()
    
    def run_menu(self):
        """Executar o loop do menu até que o jogador faça uma escolha."""
        self.running = True
        self.menu.state = MenuState.ACTIVE
        self.menu.initialize_menu_items()
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = (current_time - self.last_time) * 1000.0  # Delta time in milliseconds
            self.last_time = current_time
            
            # Process events
            self.handle_events()
            
            # Render
            selected_bot = self.menu.get_bot_name() 
            self.view.draw(self.menu, dt, selected_bot)
            
            # Cap the frame rate
            pygame.time.Clock().tick(60)
        
        # Return the menu state and player choices
        return self.menu.get_state(), self.menu.get_player_type(), self.menu.get_bot_type()