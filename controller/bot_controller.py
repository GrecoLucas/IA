from constants import *
import copy

# Helper function for logging messages both to console and game
def log_message(bot, message):
    print(message)
    if hasattr(bot.game, 'add_message'):
        bot.game.add_message(message)

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

                    
                    
    
        
    
    def  play_greedy(self):

        if self.bot.state == "deciding":
            best_move = self.bot.find_best_greedy()
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                self.bot.state = "executing"
            else:
                self.bot.game.game_over = True
        elif self.bot.state == "executing":
            return self.execute_move()

    # Faz o bfa de forma difernete, calcula primeiro o caminho completo e depois executa
    # o caminho calculado - terminal tem prints para informação
    def play_bfa(self):
        current_level = self.bot.game.level_num
        if not hasattr(self.bot, 'bfa_solution_path') or self.bot.bfa_solution_path is None or hasattr(self.bot, 'last_level') and self.bot.last_level != current_level:
            
            self.bot.last_level = current_level
            self.bot.bfa_solution_path = self._find_complete_solution_path()
            
            if self.bot.bfa_solution_path:
                log_message(self.bot, f"[BFA] Solução encontrada! {len(self.bot.bfa_solution_path)} movimentos necessários.")
                self.bot.bfa_current_move = 0
            else:
                log_message(self.bot, "[BFA] Não foi possível encontrar uma solução.")
                return
        
        if self.bot.state == "deciding":
            if not self.bot.bfa_solution_path:
                self.bot.game.game_over = True
                return
            
            # Take the next move from our pre-calculated path
            best_move = self.bot.bfa_solution_path.pop(0)
            
            if hasattr(self.bot, 'bfa_total_moves') and hasattr(self.bot, 'bfa_current_move'):
                self.bot.bfa_current_move += 1
                moves_remaining = len(self.bot.bfa_solution_path)
                if moves_remaining > 0:
                    log_message(self.bot, f"[BFA] Executando movimento {self.bot.bfa_current_move}/{self.bot.bfa_total_moves}.")
                else:
                    log_message(self.bot, f"[BFA] Executando movimento {self.bot.bfa_current_move}/{self.bot.bfa_total_moves}.")
                    log_message(self.bot, "Aperte 'P' para procurar a solução.")
            else:
                if not hasattr(self.bot, 'bfa_total_moves'):
                    self.bot.bfa_total_moves = len(self.bot.bfa_solution_path) + 1  # +1 para o movimento atual
                if not hasattr(self.bot, 'bfa_current_move'):
                    self.bot.bfa_current_move = 1
                log_message(self.bot, f"[BFA] Executando movimento {self.bot.bfa_current_move}/{self.bot.bfa_total_moves}.")
            
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                self.bot.state = "executing"
            else:
                log_message(self.bot, "[BFA] Movimento inválido encontrado.")
                self.bot.game.game_over = True
        
        elif self.bot.state == "executing":
            return self.execute_move()
    
    def _find_complete_solution_path(self):
        game_copy = copy.deepcopy(self.bot.game)
        
        solution_path = []
        max_moves = MAX_BFA_MOVES
        moves_made = 0
        
        # Inicializa contadores para informação do usuário
        if not hasattr(self.bot, 'bfa_total_moves'):
            self.bot.bfa_total_moves = 0
        if not hasattr(self.bot, 'bfa_current_move'):
            self.bot.bfa_current_move = 0
        
        while not game_copy.check_level_complete() and not game_copy.game_over and moves_made < max_moves:
            # Create a temporary bot for finding the next move
            temp_bot = copy.deepcopy(self.bot)
            temp_bot.game = game_copy
            
            # Find the next best move using BFA, with fallback to greedy
            next_move = temp_bot.find_best_bfa()
            
            # Se BFA falhar, tente com greedy
            if not next_move:
                log_message(self.bot, "[BFA] BFA falhou, tentando greedy...")
                next_move = temp_bot.find_best_greedy()
                
            if not next_move:
                log_message(self.bot, "[BFA] Buscando qualquer movimento válido...")
                has_valid_moves = False
                for block_index, block in enumerate(game_copy.available_blocks):
                    if block is None:
                        continue
                    for y in range(GRID_HEIGHT):
                        for x in range(GRID_WIDTH):
                            if game_copy.is_valid_position(block, x, y):
                                has_valid_moves = True
                                next_move = (block_index, x, y)
                                break
                        if has_valid_moves:
                            break
                    if has_valid_moves:
                        break
                        
                if not has_valid_moves:
                    log_message(self.bot, "[BFA] Realmente não há movimentos válidos.")
                    return None
            
            # Add this move to our solution path
            solution_path.append(next_move)
            
            # Log do movimento sendo realizado
            block_index, x, y = next_move
            
            # Apply the move to our simulation
            move_success = game_copy.make_move(block_index, x, y)
            if not move_success:
                log_message(self.bot, f"[BFA] Erro: movimento {moves_made+1} falhou!")
                return None
            
            # Get new blocks if needed
            if game_copy.all_blocks_used():
                game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
            
            # Check if level is complete
            if game_copy.check_level_complete():
                self.bot.bfa_total_moves = len(solution_path)
                break
            
            moves_made += 1

        
        if moves_made >= max_moves:
            log_message(self.bot, f"[BFA] Falha: Limite de {max_moves} movimentos excedido")
            return None
        
        if game_copy.game_over:
            log_message(self.bot, "[BFA] Falha: Game over na simulação")
            return None
        
        return solution_path
    
    def play(self):
        match self.bot.algorithm:
            case BotType.RANDOM:
                self.play_random()  
                self.play_random() 
            case BotType.OPTIMAL:
                self.play_optimal()
                self.play_optimal()
            
            case BotType.ITERATIVE:  
                self.play_iterative()
                
            case BotType.GREEDY:
                self.play_greedy()
                self.play_greedy()
            case BotType.BFA:
                self.play_bfa()
                self.play_bfa()
            case _:
                pass
        return

