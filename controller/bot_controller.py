import pygame
from constants import BOARD_X, BOARD_Y, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
import random
class BotController:
    def __init__(self, game):
        self.game = game
        #self.view = view
        #self.dragging = False
        #self.selected_block_index = -1  # Track which block was selected
        self.animation_delay = 100  # ms
    
    def get_possible_positions_block(self, block):
        valid = False
        tries = 100
        while not valid and tries > 0:
            x = random.randint(0,GRID_WIDTH-1)
            y = random.randint(0,GRID_HEIGHT-1)
            #grid_x = (x - BOARD_X) // GRID_SIZE
            #grid_y = (y - BOARD_Y) // GRID_SIZE
            valid = self.game.is_valid_position(block, x, y)
            tries -= 1
        if not valid:
            return False # no valid positions for selected block
        else:
            print(f"positions: x:{x}, y:{y}")
            return (x,y)


    def choose_random_block(self):
        blocks = [b for b in self.game.available_blocks]
        if not blocks:
            print("no blocks obtained in choose_random_block")
            #self.game.over= True
            # IMPLEMENTAR GAME OVER PARA SITUAÇÃO IMPOSSIVEL FICAR SEM BLOCOS
            return False
        else:
            avail = [0,1,2] # BLOCK INDEXES
            while len(avail) > 0:
                i = random.randint(0, len(avail)-1)  # Choose a random index from avail list
                selected_index = avail.pop(i)
                candidate_block = blocks[selected_index]
                if candidate_block is None:
                    continue
                pos = self.get_possible_positions_block(candidate_block)
                if pos:   #  Posição encontrada para fazer uma jogada
                    x,y = pos
                    #print(f"x: {x} || y:{y}")
                    #placement_pos = (x,y)
                    return (candidate_block, selected_index, x, y) #(candidate_block, placement_pos)
            return False

                        

    def play(self):
        move = self.choose_random_block()
        if move:
            print(f"pos:{move}")
            #block,x, y = pos
            #(block, ) = move
            #x,y = pos
            #print(f"pos_x: {x}, pos_y: {y}")
            #block=self.game.available_blocks[0]
            return move
        else:
            print("choose_random_move returned False")
            return False
        """
        block=self.game.available_blocks[0]
        pos = self.get_possible_positions_block(block)
        animation_needed = False
        if pos:   #  Posição encontrada para fazer uma jogada
            x,y = pos
            print(f"x:{x}, y:{y}")
            return (block, pos)
            #return (block, 0)
            self.game.selected_block = block
            animation_needed = self.game.place_block(self.game.selected_block, x, y)
        else:
            print("fail")
        return animation_needed"
        """
