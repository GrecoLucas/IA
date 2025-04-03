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

    # Main application loop to allow returning to menu
    running = True
    while running:
        # Set up menu system
        menu_model = Menu()
        menu_view = MenuView(screen)
        menu_controller = MenuController(menu_model, menu_view)
        
        # Run menu until game starts or exit is selected
        menu_state, player_type, bot_type = menu_controller.run_menu()

        # Handle menu result
        if menu_state == MenuState.EXIT:
            running = False
            break

        # Create MVC components for the game
        game = Game()
        game.set_player_type(player_type)
        view = GameView(screen)

        # Choose controller based on player type
        if player_type == PlayerType.BOT:
            algorithm = bot_type
            bot = Bot(game, algorithm)
            bot_controller = BotController(bot)
            controller = GameController(game, view, bot_controller)
            game.set_bot_type(algorithm) 
        else:
            controller = GameController(game, view)

        selected_level = menu_model.get_selected_level()
        game.load_level(selected_level if selected_level > 0 else 0)
        
        clock = pygame.time.Clock()
        game_running = True
        
        # Game loop
        while game_running:
            # Process all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Only pass actual events to the controller
                controller.handle_event(event)

            # Check if we need to return to menu
            if controller.return_to_menu:
                game_running = False
                
            view.render(game)
            pygame.display.flip()

            #controller.update()

            clock.tick(60)
            if game.game_over or game.game_won:
                controller.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
