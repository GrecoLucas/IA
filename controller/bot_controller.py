import pygame
from constants import BOARD_X, BOARD_Y, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
import random
class BotController:

    def __init__(self, bot):
        self.bot = bot
        self.iterative_seq = []
        self.iterative_idx = 0

    def reset(self):
        self.iterative_seq = []
        self.iterative_idx = 0
        self.bot.reset()
        
    def execute_move(self):
        if self.bot.game.make_move(self.bot.selected_block_index, self.bot.target_x, self.bot.target_y):
                self.bot.game.selected_block = None
                
                if self.bot.game.check_level_complete():
                    next_level = self.bot.game.get_next_level()
                    if next_level is not None:
                        self.bot.game.load_level(next_level)
                    else:
                        self.bot.game.game_won = True
                elif self.bot.game.all_blocks_used():
                    self.bot.game.available_blocks = self.bot.game.get_next_blocks_from_sequence()
 
        self.bot.state = "deciding"
        move_made = True
            
        return move_made  # Retorna se uma atualização visual é necessária
                        

    def play_random(self):
        
        if self.bot.state == "deciding":
            move = self.bot.choose_random_block()
            if move:
                self.bot.game.selected_block, self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = move
                self.bot.state = "executing"
                
            else:
                self.bot.game.game_over = True

        elif self.bot.state == "executing":
            return self.execute_move()        
        
        

    def play_optimal(self):
       
        if self.bot.state == "deciding":
            best_move = self.bot.find_best_move()
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                self.bot.state = "executing"
            else:
                self.bot.game.game_over = True
                
        elif self.bot.state == "executing":
            return self.execute_move()
        
    def play_iterative(self):
        if self.bot.state == "deciding":
            print("HIHIHIHIIHIHIHIHIH")
            move_sequence = self.bot.iterative_deepening_search(8)
            if move_sequence is not None:
                self.iterative_seq = move_sequence
                self.bot.state = "executing"
                self.play_iterative()
                
            else:
                self.bot.game.game_over = True

        elif self.bot.state == "executing":
                # garante que nunca é feito um acesso fora do array
                if self.iterative_idx < len(self.iterative_seq):
                    print(f"move {self.iterative_seq}")
                    move = self.iterative_seq[self.iterative_idx]
                    self.bot.selected_block_index, self.bot.target_x, self.bot.target_y  = move
                    self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                    move_made = self.execute_move()
                    self.bot.state = "executing"
                    self.iterative_idx += 1 # Atualiza o bloco em que está

                    
                    
    
        
    def play(self):
        match self.bot.algorithm:
            case "random":
                self.play_random() # Estado "deciding"
                self.play_random() # Estdo "executing"
            case "optimal":
                self.play_optimal()
                self.play_optimal()
            case "iterative":
                
                self.play_iterative()
                

