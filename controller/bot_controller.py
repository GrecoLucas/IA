from constants import *
import copy
import pygame

# Helper function for logging messages both to console and game
def log_message(bot, message):
    print(message)
    if hasattr(bot.game, 'add_message'):
        bot.game.add_message(message)

class BotController:

    def __init__(self, bot):
        self.bot = bot
        self.bot_move_seq = []
        self.move_seq_idx = 0
        self.preview_start_time = None

    def reset(self):
        self.bot_move_seq = []
        self.move_seq_idx = 0
        self.bot.reset()
    
    def get_bot(self):
        return self.bot
      
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
                        
    def play_random(self, view):
        if self.bot.state == "deciding":
            move = self.bot.choose_random_block()
            if move:
                self.bot.game.selected_block, self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = move
                #self.preview_start_time = pygame.time.get_ticks()
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                self.bot.state = "executing"
            else:
                self.bot.game.game_over = True
        elif self.bot.state == "executing":
            view.clear_hint()
            return self.execute_move()        
        
    def play_optimal(self, view):
        if self.bot.state == "deciding":
            best_move = self.bot.find_best_move()
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                self.bot.state = "executing"
            else:
                self.bot.game.game_over = True
        elif self.bot.state == "executing":
            view.clear_hint()
            return self.execute_move()
        
    def play_iterative(self):
        if self.bot.state == "deciding":
            move_sequence = self.bot.iterative_deepening_search(1,10* self.bot.game.current_level.difficulty)
            if move_sequence is not None:
                self.bot_move_seq = move_sequence
                print(f"move_seq: {self.bot_move_seq}")
                self.bot.state = "executing"
                self.play_iterative()
                
            else:
                self.bot.game.game_over = True

        elif self.bot.state == "executing":
                # garante que nunca é feito um acesso fora do array
                if self.move_seq_idx < len(self.bot_move_seq):
                    move = self.bot_move_seq[self.move_seq_idx]
                    self.bot.selected_block_index, self.bot.target_x, self.bot.target_y  = move
                    self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                    move_made = self.execute_move()
                    
                    # Para o último movimento, o estado deve voltar a "deciding" para o bot calcular a próxima sequencia de movimentos no nível seguinte
                    if  self.move_seq_idx < len(self.bot_move_seq) - 1:
                        self.bot.state = "executing"
                        self.move_seq_idx += 1 # Atualiza o bloco em que está
                    elif self.move_seq_idx == len(self.bot_move_seq) - 1:
                        self.move_seq_idx = 0

                    
                    
    
        
    
    def  play_greedy(self, view):

        if self.bot.state == "deciding":
            best_move = self.bot.find_best_greedy()
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                self.bot.state = "executing"
            else:
                self.bot.game.game_over = True
        elif self.bot.state == "executing":
            view.clear_hint()
            return self.execute_move()

    # Faz o bfa de forma difernete, calcula primeiro o caminho completo e depois executa
    # o caminho calculado - terminal tem prints para informação
    def play_bfa(self, view):
        current_level = self.bot.game.level_num
        
        # Add the print_once attribute if it doesn't exist
        if not hasattr(self, 'print_once'):
            self.print_once = False
            
        # Check if game ended and save stats if needed
        if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
            self.bot.game.save_game_stats()
            self.print_once = True
            print("[DEBUG] Saved game statistics in automatic mode")
            return
        
        if not hasattr(self.bot, 'bfa_solution_path') or self.bot.bfa_solution_path is None or hasattr(self.bot, 'last_level') and self.bot.last_level != current_level:
            
            self.bot.last_level = current_level
            self.bot.bfa_solution_path = self._find_complete_solution_path()
            
            if self.bot.bfa_solution_path:
                log_message(self.bot, f"[BFA] Solução encontrada! {len(self.bot.bfa_solution_path)} movimentos necessários.")
                self.bot.bfa_current_move = 0
            else:
                log_message(self.bot, "[BFA] Não foi possível encontrar uma solução.")
                # Mark game as over when no solution found
                self.bot.game.game_over = True
                # Save stats when game is over due to no solution
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after no solution found")
                return
        
        if self.bot.state == "deciding":
            if not self.bot.bfa_solution_path:
                self.bot.game.game_over = True
                # Save stats when game is over due to empty solution path
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after empty solution path")
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
                # Draw preview
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                self.bot.state = "executing"
            else:
                log_message(self.bot, "[BFA] Movimento inválido encontrado.")
                self.bot.game.game_over = True
                # Save stats when game is over due to invalid move
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after invalid move")
        
        elif self.bot.state == "executing":
            view.clear_hint()
            move_result = self.execute_move()
            # Check if game ended after executing a move
            if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
                self.bot.game.save_game_stats()
                self.print_once = True
                print("[DEBUG] Saved game statistics after move execution")
            return move_result
    
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
    
    # Faz o dfs de forma difernete, calcula primeiro o caminho completo e depois executa
    # o caminho calculado - terminal tem prints para informação
    def play_dfs(self, view):
        current_level = self.bot.game.level_num
        
        # Add the print_once attribute if it doesn't exist
        if not hasattr(self, 'print_once'):
            self.print_once = False
            
        # Check if game ended and save stats if needed
        if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
            self.bot.game.save_game_stats()
            self.print_once = True
            print("[DEBUG] Saved game statistics in automatic mode")
            return
        
        if not hasattr(self.bot, 'dfs_solution_path') or self.bot.dfs_solution_path is None or hasattr(self.bot, 'last_level') and self.bot.last_level != current_level:
            
            self.bot.last_level = current_level
            self.bot.dfs_solution_path = self._find_complete_solution_path_dfs()
            
            if self.bot.dfs_solution_path:
                log_message(self.bot, f"[DFS] Solução encontrada! {len(self.bot.dfs_solution_path)} movimentos necessários.")
                self.bot.dfs_current_move = 0
            else:
                log_message(self.bot, "[DFS] Não foi possível encontrar uma solução.")
                # Mark game as over when no solution found
                self.bot.game.game_over = True
                # Save stats when game is over due to no solution
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after no solution found")
                return
        
        if self.bot.state == "deciding":
            if not self.bot.dfs_solution_path:
                self.bot.game.game_over = True
                # Save stats when game is over due to empty solution path
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after empty solution path")
                return
            
            # Take the next move from our pre-calculated path
            best_move = self.bot.dfs_solution_path.pop(0)
            
            if hasattr(self.bot, 'dfs_total_moves') and hasattr(self.bot, 'dfs_current_move'):
                self.bot.dfs_current_move += 1
                moves_remaining = len(self.bot.dfs_solution_path)
                if moves_remaining > 0:
                    log_message(self.bot, f"[DFS] Executando movimento {self.bot.dfs_current_move}/{self.bot.dfs_total_moves}.")
                else:
                    log_message(self.bot, f"[DFS] Executando movimento {self.bot.dfs_current_move}/{self.bot.dfs_total_moves}.")
                    log_message(self.bot, "Aperte 'P' para procurar a solução.")
            else:
                if not hasattr(self.bot, 'dfs_total_moves'):
                    self.bot.dfs_total_moves = len(self.bot.dfs_solution_path) + 1  # +1 para o movimento atual
                if not hasattr(self.bot, 'dfs_current_move'):
                    self.bot.dfs_current_move = 1
                log_message(self.bot, f"[DFS] Executando movimento {self.bot.dfs_current_move}/{self.bot.dfs_total_moves}.")
            
            if best_move:
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y = best_move
                # UTIL PARA INFORMAÇÃO
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                self.bot.state = "executing"
            else:
                log_message(self.bot, "[DFS] Movimento inválido encontrado.")
                self.bot.game.game_over = True
                # Save stats when game is over due to invalid move
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after invalid move")
        
        elif self.bot.state == "executing":
            view.clear_hint()
            move_result = self.execute_move()
            # Check if game ended after executing a move
            if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
                self.bot.game.save_game_stats()
                self.print_once = True
                print("[DEBUG] Saved game statistics after move execution")
            return move_result
    
    def _find_complete_solution_path_dfs(self):
        game_copy = copy.deepcopy(self.bot.game)
        
        solution_path = []
        max_moves = MAX_DFS_MOVES
        moves_made = 0
        
        # Inicializa contadores para informação do usuário
        if not hasattr(self.bot, 'dfs_total_moves'):
            self.bot.dfs_total_moves = 0
        if not hasattr(self.bot, 'dfs_current_move'):
            self.bot.dfs_current_move = 0
        
        while not game_copy.check_level_complete() and not game_copy.game_over and moves_made < max_moves:
            # Create a temporary bot for finding the next move
            temp_bot = copy.deepcopy(self.bot)
            temp_bot.game = game_copy
            
            # Find the next best move using BFA, with fallback to greedy
            next_move = temp_bot.find_best_dfs()
            
            # Se BFA falhar, tente com greedy
            if not next_move:
                log_message(self.bot, "[DFS] DFS falhou, tentando greedy...")
                next_move = temp_bot.find_best_greedy()
                
            if not next_move:
                log_message(self.bot, "[DFS] Buscando qualquer movimento válido...")
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
                    log_message(self.bot, "[DFS] Realmente não há movimentos válidos.")
                    return None
            
            # Add this move to our solution path
            solution_path.append(next_move)
            
            # Log do movimento sendo realizado
            block_index, x, y = next_move
            
            # Apply the move to our simulation
            move_success = game_copy.make_move(block_index, x, y)
            if not move_success:
                log_message(self.bot, f"[DFS] Erro: movimento {moves_made+1} falhou!")
                return None
            
            # Get new blocks if needed
            if game_copy.all_blocks_used():
                game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
            
            # Check if level is complete
            if game_copy.check_level_complete():
                self.bot.dfs_total_moves = len(solution_path)
                break
            
            moves_made += 1

        
        if moves_made >= max_moves:
            log_message(self.bot, f"[DFS] Falha: Limite de {max_moves} movimentos excedido")
            return None
        
        if game_copy.game_over:
            log_message(self.bot, "[DFS] Falha: Game over na simulação")
            return None
        
        return solution_path

    

    def play_a_star(self, view):

        # Add the print_once attribute if it doesn't exist
        if not hasattr(self, 'print_once'):
            self.print_once = False
            
        # Check if game ended and save stats if needed
        if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
            self.bot.game.save_game_stats()
            self.print_once = True
            print("[DEBUG] Saved game statistics in automatic mode")
            return
        

        if self.bot.state == "deciding":
            move_sequence = self.bot.a_star_search()

            if move_sequence is not None:
                
                self.bot_move_seq = move_sequence
                log_message(self.bot, f"[A STAR] Solução encontrada! {len(move_sequence)} movimentos necessários.")
                #print(f"move_seq: {self.bot_move_seq}")
                self.bot.state = "executing"
                move = self.bot_move_seq[self.move_seq_idx]
                self.bot.selected_block_index, self.bot.target_x, self.bot.target_y  = move
                self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                #self.play_a_star(view)
                
            else:
                log_message(self.bot, "[A STAR] Não foi possível encontrar uma solução.")
                self.bot.game.game_over = True
                # Save stats when game is over due to no solution
                if self.print_once == False:
                    self.bot.game.save_game_stats()
                    self.print_once = True
                    print("[DEBUG] Saved game statistics after no solution found")
        
        elif self.bot.state == "executing":
                # garante que nunca é feito um acesso fora do array
                if self.move_seq_idx < len(self.bot_move_seq):
                    view.clear_hint()
                    """move = self.bot_move_seq[self.move_seq_idx]
                    self.bot.selected_block_index, self.bot.target_x, self.bot.target_y  = move
                    self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]"""
                    
                    
                    log_message(self.bot, f"[A STAR] Executando movimento {self.move_seq_idx + 1}.")
                    """"self.preview_start_time = pygame.time.get_ticks()
                    current_time = pygame.time.get_ticks()
                    while (current_time - self.preview_start_time) < 3000:
                        current_time = pygame.time.get_ticks()"""
                    

                    self.execute_move()
                    
                    # Para o último movimento, o estado deve voltar a "deciding" para o bot calcular a próxima sequencia de movimentos no nível seguinte
                    if  self.move_seq_idx < len(self.bot_move_seq) - 1:
                        log_message(self.bot, "Aperte 'P' para ver a próxima jogada.")
                        self.bot.state = "executing"
                        self.move_seq_idx += 1 # Atualiza o bloco em que está
                        # get next move's info and display the preview
                        move = self.bot_move_seq[self.move_seq_idx]
                        self.bot.selected_block_index, self.bot.target_x, self.bot.target_y  = move
                        self.bot.game.selected_block = self.bot.game.available_blocks[self.bot.selected_block_index]
                        view.set_hint(self.bot.game.selected_block, self.bot.target_x, self.bot.target_y)
                        
                    elif self.move_seq_idx == len(self.bot_move_seq) - 1:
                        log_message(self.bot, "Aperte 'P' para procurar a solução.")
                        self.move_seq_idx = 0

                    if (self.bot.game.game_over or self.bot.game.game_won) and self.print_once == False:
                        self.bot.game.save_game_stats()
                        self.print_once = True
                        print("[DEBUG] Saved game statistics after move execution")
                    


    def play(self, view):
        match self.bot.algorithm:
            case BotType.RANDOM:
                self.play_random(view)

            case BotType.OPTIMAL:
                self.play_optimal(view)
            
            case BotType.ITERATIVE:  
                self.play_iterative()
                
            case BotType.GREEDY:
                self.play_greedy(view)

            case BotType.BFA:
                self.play_bfa(view)
                
            case BotType.DFS:
                self.play_dfs(view)

            case BotType.ASTAR:
                print(" STAR CHOSEN")
                self.play_a_star(view)
            
            case _:
                pass
        return

