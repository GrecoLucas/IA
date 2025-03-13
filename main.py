import pygame
import sys
from model.game import Game
from view.game_view import GameView
from controller.game_controller import GameController
from controller.bot_controller import BotController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from view.menu_view import MenuView
from model.menu import Menu, MenuState, PlayerType 
from controller.menu_controller import MenuController
from model.bot import Bot  

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
        algorithm = "optimal"  #"random" 
        bot = Bot(game, algorithm)
        bot_controller = BotController(bot)
        controller = GameController(game, view, bot_controller)
    else:  
        controller = GameController(game, view)
    
    game.load_level(0)  # Carregar o primeiro nível
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            controller.handle_event(event)

        view.render(game)
        pygame.display.flip()
        
        controller.update()

        clock.tick(60)

if __name__ == "__main__":
    main()