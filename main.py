import pygame
import sys
from model.game import Game
from view.game_view import GameView
from controller.game_controller import GameController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from view.menu_view import MenuView
from model.menu import Menu, MenuState, PlayerType  # Adicionando a importação de MenuState e PlayerType
from controller.menu_controller import MenuController

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wood Block")
    
    # Menu
    menu_model = Menu()
    menu_view = MenuView(screen)
    menu_controller = MenuController(menu_model, menu_view)
    
    menu_state, player_type = menu_controller.run_menu()

    # Verificar o resultado do menu
    if menu_state == MenuState.EXIT:
        pygame.quit()
        sys.exit()

    # Create MVC components
    game = Game()
    game.set_player_type(player_type)
    view = GameView(screen)
    
    # Escolher o tipo de controlador baseado na escolha do jogador
    if player_type == PlayerType.BOT:
        print("Not implemented yet")
        sys.exit()
    else:  # Jogador humano
        controller = GameController(game, view)
    
    if (menu_state == MenuState.GAME_START_INF):
        game.load_level(-1)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Pass events to the controller
            controller.handle_event(event)
        
        # Update game state
        controller.update()
        
        # Render game
        view.render(game)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()