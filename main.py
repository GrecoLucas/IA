import pygame
import sys
from model.game import Game
from view.game_view import GameView
from controller.game_controller import GameController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wood Block - Puzzle Games")
    
    # Create MVC components
    game = Game()
    view = GameView(screen)
    controller = GameController(game, view)
    
    # Game loop
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
