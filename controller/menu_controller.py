import pygame
from model.menu import MenuState
from model.menu import MenuState, PlayerType  
class MenuController:
    def __init__(self, menu, menu_view):
        self.menu = menu
        self.menu_view = menu_view
        self.selected_bot_name = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu.move_selection(-1)
                elif event.key == pygame.K_DOWN:
                    self.menu.move_selection(1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.menu.select_current()


    def run_menu(self):
        clock = pygame.time.Clock()

        while self.menu.get_state() != MenuState.EXIT and self.menu.get_state() != MenuState.GAME_START:
            dt = clock.tick(60)
            self.handle_events()  

            if self.menu.get_state() == MenuState.ACTIVE:
                self.menu_view.draw(self.menu, dt, selected_bot_name=self.get_bot_name())
            elif self.menu.get_state() == MenuState.CHOOSE_ALGORITHM:
                self.menu_view.draw(self.menu, dt, selected_bot_name=self.get_bot_name())


        return self.menu.get_state(), self.menu.get_player_type(), self.menu.get_bot_type()

    def get_bot_name(self):
        if self.menu.get_player_type() == PlayerType.BOT:
            return self.menu.get_bot_name()
        return None