from constants import *
import copy
import random
import heapq
from collections import deque

class Bot:
    def __init__(self, game, algorithm):
        self.game = game
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        self.selected_block_index = None
        self.target_x = None
        self.target_y = None
        self.state = "deciding"
        self.algorithm = algorithm
        
    def evaluate_move(self, game, green_gained, red_gained, level_advanced, moves_count=1, is_greedy=False):
        score = 0
        
        if level_advanced:
            return float('inf')
        
        # Pontos por pedras coletadas
        score += green_gained * 50
        score += red_gained * 50
        
        # Penalidade por número de movimentos (para simulações completas)
        if not is_greedy:
            score -= moves_count * 5
        
        # Bônus/Penalidade pelo estado final do jogo
        if game.game_won:
            return float('inf')
        if game.game_over:
            return float('-inf')

        return score
    
    def find_best_greedy(self):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        possible_moves = []
        
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        
        if not possible_moves:
            return None
        
        # Verificar primeiro os movimentos que avançam de nível instantaneamente
        for move in possible_moves:
            block_index, x, y = move
            
            # Criar uma cópia do estado atual do jogo
            game_copy = copy.deepcopy(self.game)
            
            # Fazer o movimento
            block = game_copy.available_blocks[block_index]
            level_before = game_copy.level_num
            
            # Executar o movimento
            game_copy.place_block(block, x, y)
            
            # Se avançou de nível imediatamente, retorne este movimento
            if game_copy.level_num > level_before:
                return move
        
        # Dicionário para armazenar a pontuação de cada movimento
        move_scores = {}
        
        # Avaliar cada movimento possível
        for move in possible_moves:
            block_index, x, y = move
            
            # Criar uma cópia do estado atual do jogo
            game_copy = copy.deepcopy(self.game)
            
            # Fazer o movimento inicial
            block = game_copy.available_blocks[block_index]
            
            # Armazenar estado antes do movimento para comparação
            green_before = game_copy.green_stones_collected
            red_before = game_copy.red_stones_collected
            level_before = game_copy.level_num
            
            # Executar o movimento
            game_copy.place_block(block, x, y)
            game_copy.available_blocks[block_index] = None
            
            # Calcular pontos ganhos com este movimento
            green_gained = game_copy.green_stones_collected - green_before
            red_gained = game_copy.red_stones_collected - red_before
            level_advanced = game_copy.level_num > level_before
            
            # Usar a função centralizada de avaliação
            simulation_score = self.evaluate_move(
                game_copy, 
                green_gained, 
                red_gained, 
                level_advanced,
                1,  # Um único movimento
                is_greedy=True
            )
            
            # Armazenar a pontuação para este movimento
            move_scores[move] = simulation_score

        # Retornar o movimento com a melhor pontuação
        if not move_scores:
            return random.choice(possible_moves) if possible_moves else None
        
        best_move = max(move_scores.items(), key=lambda x: x[1])[0]
        return best_move

        self.algorithm =  algorithm

    def reset(self):
        self.selected_block_index = None
        self.target_x = None
        self.target_y = None
        self.state = "deciding"
        
    def find_best_move(self):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        possible_moves = []
    
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
    
        if not possible_moves:
            return None
        
        # Verificar primeiro os movimentos que avançam de nível instantaneamente
        for move in possible_moves:
            block_index, x, y = move
            
            # Criar uma cópia do estado atual do jogo
            game_copy = copy.deepcopy(self.game)
            
            # Fazer o movimento
            block = game_copy.available_blocks[block_index]
            level_before = game_copy.level_num
            
            # Executar o movimento
            game_copy.place_block(block, x, y)
            
            # Se avançou de nível imediatamente, retorne este movimento
            if game_copy.level_num > level_before:
                return move
        
        # Número de simulações por movimento
        num_simulations = MAX_SIMULATION_DEPTH
        # Dicionário para armazenar a pontuação média de cada movimento
        move_scores = {}
        # Rastreia movimentos que avançam de nível durante simulações
        level_advancing_moves = []
    
        # Avaliar cada movimento possível
        for move in possible_moves:
            total_score = 0
            block_index, x, y = move
            found_level_advance = False
    
            # Executar várias simulações para este movimento
            for sim_num in range(num_simulations):
                # Criar uma cópia do estado atual do jogo
                game_copy = copy.deepcopy(self.game)
                
                # Fazer o movimento inicial
                block = game_copy.available_blocks[block_index]
                
                # Armazenar estado antes do movimento para comparação
                green_before = game_copy.green_stones_collected
                red_before = game_copy.red_stones_collected
                level_before = game_copy.level_num
                
                # Executar o movimento
                game_copy.place_block(block, x, y)
                game_copy.available_blocks[block_index] = None
                moves_count = 1  # Contamos o movimento inicial
                
                # Calcular pontos ganhos com este movimento
                green_gained = game_copy.green_stones_collected - green_before
                red_gained = game_copy.red_stones_collected - red_before
                level_advanced = game_copy.level_num > level_before
                
                # Se avançou de nível imediatamente, marque este movimento como prioritário
                if level_advanced:
                    found_level_advance = True
                    if move not in level_advancing_moves:
                        level_advancing_moves.append(move)
                    break  # Não precisamos de mais simulações
                
                # Atualizar blocos disponíveis se necessário
                if game_copy.all_blocks_used():
                    game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
                
                # Simular o restante do jogo com movimentos aleatórios
                max_simulation_depth = MAX_SIMULATION_DEPTH
                simulation_depth = 0
                
                while not game_copy.game_over and not game_copy.game_won and simulation_depth < max_simulation_depth:
                    sim_possible_moves = []
                    for sim_block_index, sim_block in enumerate(game_copy.available_blocks):
                        if sim_block is None:
                            continue
                        for sim_y in range(self.grid_height):
                            for sim_x in range(self.grid_width):
                                if game_copy.is_valid_position(sim_block, sim_x, sim_y):
                                    sim_possible_moves.append((sim_block_index, sim_x, sim_y))
                    
                    if not sim_possible_moves:
                        break
                    
                    # Escolher um movimento aleatório
                    sim_block_index, sim_x, sim_y = random.choice(sim_possible_moves)
                    sim_block = game_copy.available_blocks[sim_block_index]
                    
                    # Armazenar estado antes do movimento para comparação
                    green_before = game_copy.green_stones_collected
                    red_before = game_copy.red_stones_collected
                    level_before = game_copy.level_num
                    
                    # Fazer o movimento
                    game_copy.place_block(sim_block, sim_x, sim_y)
                    game_copy.available_blocks[sim_block_index] = None
                    moves_count += 1
                    
                    # Calcular pontos ganhos com este movimento
                    green_gained += game_copy.green_stones_collected - green_before
                    red_gained += game_copy.red_stones_collected - red_before
                    
                    # Verificar se avançou de nível durante a simulação
                    if game_copy.level_num > level_before:
                        level_advanced = True
                        found_level_advance = True
                        if move not in level_advancing_moves:
                            level_advancing_moves.append(move)
                        break  # Não precisamos continuar esta simulação
                    
                    # Se todos os blocos foram usados, obter novos
                    if game_copy.all_blocks_used():
                        game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
                    
                    simulation_depth += 1
                
                # Se encontramos avanço de nível, não precisamos de mais simulações
                if found_level_advance:
                    break
                
                # Usar a função centralizada de avaliação
                simulation_score = self.evaluate_move(
                    game_copy,
                    green_gained,
                    red_gained,
                    level_advanced,
                    moves_count,
                    is_greedy=False
                )
                
                total_score += simulation_score
            
            # Se este movimento leva a um avanço de nível em alguma simulação
            if found_level_advance:
                move_scores[move] = float('inf')  # Prioridade máxima
            else:
                # Armazenar a pontuação média para este movimento
                simulations_run = sim_num + 1
                move_scores[move] = total_score / simulations_run
        
        # Priorizar movimentos que levam a avanço de nível
        if level_advancing_moves:
            return random.choice(level_advancing_moves)
        
        # Retornar o movimento com a melhor pontuação média
        if not move_scores:
            return random.choice(possible_moves) if possible_moves else None
            
        best_move = max(move_scores.items(), key=lambda x: x[1])[0]
        return best_move
    

    ### BOT  BFA ------------------------------
    def find_best_bfa(self):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        # Cache de soluções para evitar recomputação
        if not hasattr(self.__class__, 'bfa_cache'):
            self.__class__.bfa_cache = {}

        # Gerar uma chave única para o estado atual do jogo
        game_state_key = self._create_game_state_key(self.game)

        # Verificar se já temos uma solução em cache para este estado
        if game_state_key in self.__class__.bfa_cache:
            return self.__class__.bfa_cache[game_state_key]

        possible_moves = []

        # Coletar todos os movimentos possíveis para o estado atual do jogo
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))

        if not possible_moves:
            # Não há movimentos possíveis, marcar o jogo como terminado se não estiver ganho
            if not self.game.game_won:
                self.game.game_over = True
            self.__class__.bfa_cache[game_state_key] = None
            return None

        # Verificar primeiro os movimentos que avançam de nível instantaneamente
        for move in possible_moves:
            block_index, x, y = move

            # Criar uma cópia do estado atual do jogo
            game_copy = copy.deepcopy(self.game)

            # Fazer o movimento
            block = game_copy.available_blocks[block_index]
            level_before = game_copy.level_num

            # Executar o movimento
            game_copy.place_block(block, x, y)
            game_copy.available_blocks[block_index] = None

            # Se avançou de nível imediatamente, salve no cache e retorne este movimento
            if game_copy.level_num > level_before or game_copy.check_level_complete():
                self.__class__.bfa_cache[game_state_key] = move
                return move

        # Use a fila para a busca em largura
        queue = deque([(self.game, [])])  # Tupla: (estado do jogo, caminho até aqui)
        visited_states = set()  # Rastrear estados visitados para evitar loops
        winning_paths = []  # Armazenar todos os caminhos vencedores encontrados

        while queue:
            current_game, path = queue.popleft()

            # Criar uma chave única para o estado atual
            current_state_key = self._create_game_state_key(current_game)

            # Se este estado já foi visitado, pule
            if current_state_key in visited_states:
                continue
            visited_states.add(current_state_key)

            # Se o jogo avançou de nível ou foi vencido, registre o caminho
            if current_game.check_level_complete() or current_game.game_won:
                winning_paths.append(path)
                if current_game.game_won:
                    self.game.game_won = True
                if len(path) <= 10: 
                    self.__class__.bfa_cache[game_state_key] = path[0] if path else None
                    return path[0] if path else None
                continue  

            if current_game.game_over:
                continue
            
            # Coletar todos os movimentos possíveis para o estado atual do jogo
            possible_moves = []
            for block_index, block in enumerate(current_game.available_blocks):
                if block is None:
                    continue
                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        if current_game.is_valid_position(block, x, y):
                            possible_moves.append((block_index, x, y))

            if not possible_moves:
                # Se não há movimentos possíveis e não encontramos solução, marcar como jogo terminado
                if len(winning_paths) == 0:
                    current_game.game_over = True
                    # Propagar esse estado para o jogo principal se necessário
                    if current_game is self.game or path == []:
                        self.game.game_over = True
                continue
            
            # Explore cada movimento possível a partir do estado atual
            for block_index, x, y in possible_moves:
                game_copy = copy.deepcopy(current_game)
                block = game_copy.available_blocks[block_index]

                # Armazenar estado antes do movimento
                green_before = game_copy.green_stones_collected
                red_before = game_copy.red_stones_collected
                level_before = game_copy.level_num

                # Executar o movimento
                game_copy.place_block(block, x, y)
                game_copy.available_blocks[block_index] = None

                # Verificar se este movimento resultou em progresso significativo
                progress_made = (
                    game_copy.green_stones_collected > green_before or
                    game_copy.red_stones_collected > red_before or
                    game_copy.level_num > level_before or
                    game_copy.check_level_complete()
                )

                # Se todos os blocos foram usados, obtenha os próximos
                if game_copy.all_blocks_used():
                    game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()

                # Crie um novo caminho estendendo o caminho atual
                new_path = path + [(block_index, x, y)]

                # Priorizar movimentos que fazem progresso
                if progress_made:
                    queue.appendleft((game_copy, new_path))  # Coloca no início da fila
                else:
                    queue.append((game_copy, new_path))

        best_move = None
        if winning_paths:
            shortest_path = min(winning_paths, key=len)
            if shortest_path:
                best_move = shortest_path[0]  # O primeiro movimento do caminho mais curto
        else:
            self.game.game_over = True

        # Salve a solução no cache
        self.__class__.bfa_cache[game_state_key] = best_move
        return best_move

    def find_best_dfs(self):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        # Cache de soluções para evitar recomputação
        if not hasattr(self.__class__, 'dfs_cache'):
            self.__class__.dfs_cache = {}
            
        # Gerar uma chave única para o estado atual do jogo
        game_state_key = self._create_game_state_key(self.game)
        
        # Verificar se já temos uma solução em cache para este estado
        if game_state_key in self.__class__.dfs_cache:
            return self.__class__.dfs_cache[game_state_key]
        
        possible_moves = []
        
        # Coletar todos os movimentos possíveis para o estado atual do jogo
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        
        if not possible_moves:
            # Não há movimentos possíveis, marcar o jogo como terminado se não estiver ganho
            if not self.game.game_won:
                self.game.game_over = True
            self.__class__.dfs_cache[game_state_key] = None
            return None  # Não há movimentos possíveis
        
        # Verificar primeiro os movimentos que avançam de nível instantaneamente
        for move in possible_moves:
            block_index, x, y = move
            
            # Criar uma cópia do estado atual do jogo
            game_copy = copy.deepcopy(self.game)
            
            # Fazer o movimento
            block = game_copy.available_blocks[block_index]
            level_before = game_copy.level_num
            
            # Executar o movimento
            game_copy.place_block(block, x, y)
            game_copy.available_blocks[block_index] = None
            
            # Se avançou de nível imediatamente, salve no cache e retorne este movimento
            if game_copy.level_num > level_before or game_copy.check_level_complete():
                self.__class__.dfs_cache[game_state_key] = move
                return move
        
        stack = [(self.game, [])]  # Tupla: (estado do jogo, caminho até aqui)
        visited_states = set()  # Rastrear estados visitados para evitar loops
        winning_paths = []  # Armazenar todos os caminhos vencedores encontrados
    
        while stack:
            current_game, path = stack.pop()  # Remove do topo da pilha (DFS)
            
            current_state_key = self._create_game_state_key(current_game)
            
            if current_state_key in visited_states:
                continue
            visited_states.add(current_state_key)
            
            if current_game.check_level_complete() or current_game.game_won:
                winning_paths.append(path)
                # Atualizar o estado do jogo principal se encontramos vitória
                if current_game.game_won:
                    self.game.game_won = True
                if len(path) <= 15:
                    self.__class__.dfs_cache[current_state_key] = path[0] if path else None
                    return path[0] if path else None
                continue
            
            if current_game.game_over:
                continue
            
            possible_moves = []
            for block_index, block in enumerate(current_game.available_blocks):
                if block is None:
                    continue
                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        if current_game.is_valid_position(block, x, y):
                            possible_moves.append((block_index, x, y))
            
            if not possible_moves:
                # Se não há movimentos possíveis e não encontramos solução, marcar como jogo terminado
                if len(winning_paths) == 0:
                    current_game.game_over = True
                    # Propagar esse estado para o jogo principal se necessário
                    if current_game is self.game or path == []:
                        self.game.game_over = True
                continue
            
            for block_index, x, y in reversed(possible_moves):  # Inverte para manter a ordem do DFS
                game_copy = copy.deepcopy(current_game)
                block = game_copy.available_blocks[block_index]
                
                game_copy.place_block(block, x, y)
                game_copy.available_blocks[block_index] = None

                
                if game_copy.all_blocks_used():
                    game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
                
                new_path = path + [(block_index, x, y)]
                
                stack.append((game_copy, new_path))  # DFS adiciona ao topo da pilha

    
        best_move = None
        if winning_paths:
            shortest_path = min(winning_paths, key=len)
            if shortest_path:
                best_move = shortest_path[0]
        else:
            self.game.game_over = True
        
        self.__class__.dfs_cache[game_state_key] = best_move
        return best_move
    
    def _create_game_state_key(self, game):
        # Represente o tabuleiro como uma tupla de tuplas
        board_key = tuple(tuple(row) for row in game.board_types)
        
        # Represente os blocos disponíveis como uma tupla
        blocks_key = []
        for block in game.available_blocks:
            if block is None:
                blocks_key.append(None)
            else:
                # Use shape_name em vez de shape_index que não existe na classe Block
                block_shape = tuple(tuple(row) for row in block.shape)
                blocks_key.append((block.shape_name, block_shape))
        
        blocks_key = tuple(blocks_key)
        
        # Combine os elementos em uma chave de estado única
        return hash((
            board_key,
            blocks_key,
            game.green_stones_collected,
            game.red_stones_collected,
            game.green_stones_to_collect,
            game.red_stones_to_collect,
            game.level_num
        ))
    ### ------------------------------

    # Encontrar uma posição random no tabuleiro que seja válida
    def get_possible_positions_block(self, block):
        valid = False
        tries = MAX_TRIES # Define o número máximo de tentativas para encontrar uma posição válida
        while not valid and tries > 0:
            x = random.randint(0,self.grid_width-1)
            y = random.randint(0,self.grid_height-1)
            valid = self.game.is_valid_position(block, x, y)
            tries -= 1
        if not valid:
            return False # Nenhuma posição válida é encontrada
        else:
            return (x,y)
    
    # Escolha de uma peça random dentro das peças disponíveis
    def choose_random_block(self):

        blocks = [b for b in self.game.available_blocks]
        if not blocks:
            return False
        else:
            avail = [0,1,2] # índices de blocos disponíveis
            while len(avail) > 0:
                i = random.randint(0, len(avail)-1)  # Escolhe um índice random da lista
                selected_index = avail.pop(i)   # Retira o bloco da lista
                candidate_block = blocks[selected_index]
                if candidate_block is None:
                    continue    # Bloco eleito não está disponível
                pos = self.get_possible_positions_block(candidate_block)
                if pos:   #  Posição encontrada para fazer uma jogada
                    x,y = pos
                    return (candidate_block, selected_index, x, y) 
            return False
        

    # Função auxilar para encontrar todos os movimentos possíveis
    def get_all_possible_moves(self, game):
        possible_moves = []
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        # Não foi encontrado nenhum movimento possível
        if not possible_moves:
            return None
        
        return possible_moves
    
    def get_all_possible_moves_stack(self, game):
        possible_moves = deque([])
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(game.available_blocks):
            if block is None:
                continue
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if game.is_valid_position(block, x, y):
                        possible_moves.appendleft((block_index, x, y))
        # Não foi encontrado nenhum movimento possível
        if not possible_moves:
            return None
        
        return possible_moves

    # Iterative deepening search para encontrar o melhor movimento
    def iterative_deepening_search(self, min_depth, max_depth):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        for depth in range(min_depth, max_depth+1):

            solution = self.depth_limited_search(depth)
            if solution is not None:
                return solution
        return None     #Não foi encontrada nenhuma solução para a depth máxima dada
    

    # DFS com profundidade limitada
    def depth_limited_search(self, depth):
        game_copy = copy.deepcopy(self.game)
        move_sequence = self.recursive_depth_limited_search(game_copy, depth, [])
        return move_sequence
        
    
    # Parte recursiva do DFS
    def recursive_depth_limited_search(self, game, depth, move_seq):
        if game.game_won or game.check_level_complete():
            return move_seq
        if game.game_over:
                return None
        # Nenhuma solução encontrada para a profundidade dada
        if depth == 0:
            return None
        
        possible_moves = self.get_all_possible_moves_stack(game)
        # BFS itera sobre todos os movimentos possíveis 
        if(possible_moves is None):
            return None
        while possible_moves:
            move = possible_moves.pop()
            # Criar uma cópia do estado atual do jogo passado
            game_copy = copy.deepcopy(game)
            block_index, x, y = move
            block = game_copy.available_blocks[block_index]
            # Executar o movimento
            game_copy.place_block(block, x, y)
            game_copy.available_blocks[block_index] = None
            # Adicionar movimento à lista de moves executados
            new_move_seq = move_seq + [move]
            if game_copy.check_level_complete():
                return new_move_seq
            # Atualizar blocos disponíveis se necessário
            if game_copy.all_blocks_used():
                game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
        
            result = self.recursive_depth_limited_search(game_copy, depth-1, new_move_seq)
            #if result is None:
            if result is not None:
                return result   # Sequência de movimentos válida encontrada
        # Não foi encontrada nenhuma sequência de movimentos válida para ganhar o jogo
        return None
        




    def treshold(self, game_state):
        amount_moves = 10
        dif = game_state.current_level.difficulty
        return amount_moves * dif

    def check_board_gems_pos(self, old_game_state, game_state):
        fill_reward = 0
        for y in range( self.grid_height):
            for x in range (self.grid_width):
                # Check if there's a green gem at position
                # Check if there's a red gem at position
                if game_state.board_types[y][x] == 2 or game_state.board_types[y][x] == 3:
                    old_same_row_count = 0
                    current_same_row_count = 0
                    old_same_col_count = 0
                    current_same_col_count = 0
                    # Check if row is more filled
                    for x_ in range (self.grid_width):
                        old_pos = old_game_state.board_types[y][x_]
                        if old_game_state.board[y][x_] != None and old_pos != 2 and old_pos != 3:
                            old_same_row_count += 1
                        curr_pos = game_state.board_types[y][x_]
                        if game_state.board[y][x_] != None and curr_pos != 2 and curr_pos != 3:
                            current_same_row_count += 1
                    # Check if column is more filled
                    for y_ in range (self.grid_height):
                        old_pos = old_game_state.board_types[y_][x]
                        if old_game_state.board[y_][x] != None and old_pos != 2 and old_pos != 3:
                            old_same_col_count += 1
                        curr_pos = game_state.board_types[y_][x]
                        if game_state.board[y_][x] != None and curr_pos != 2 and curr_pos != 3:
                            current_same_col_count += 1
                    row_diff = current_same_row_count - old_same_row_count
                    col_diff = current_same_col_count - old_same_col_count
                    if row_diff > 0:
                        fill_reward +=  row_diff
                    if col_diff > 0:
                        fill_reward += col_diff
        return fill_reward
    
    # Check if there were pieces placed right next to gems
    def check_board_gems_adjacent_pos(self, old_game_state, game_state):
        adjacent_reward = 0
        gem_positions = []
        # Get the positions of every gem on the board
        for y in range( self.grid_height):
            for x in range (self.grid_width):
                # Check if there's a green gem at position
                # Check if there's a red gem at position
                if game_state.board_types[y][x] == 2 or game_state.board_types[y][x] == 3:
                    gem_positions.append((y,x))
        adjacent = []
        # Get all valid adjacent positions
        for (gem_y, gem_x) in gem_positions:
            check_positions = [(gem_y, gem_x-1), (gem_y, gem_x+1), (gem_y-1, gem_x), (gem_y+1, gem_x)]
            for (y,x) in check_positions:
                if y < self.grid_height and y >= 0 and x < self.grid_width and x >= 0:
                    adjacent.append((y,x))
        # Check if piece was placed in empty pos
        for (y,x) in adjacent:
            if old_game_state.board[y][x] == None and game_state.board[y][x]:
                adjacent_reward += 1

        
        return adjacent_reward

    # Algorítmo A*
    def heuristic(self, game_state, old_game_state, cleared, current_amount_moves ):
        """Estimate the remaining steps needed to collect all green and red pieces."""
        punishment = 0
        reward = 0
        expected_amount_moves = self.treshold(game_state)
        difference = current_amount_moves - expected_amount_moves
        
        if (difference > 0):
            punishment += difference
        else:
            if cleared: 
                reward += 1*0.3 
        fill = self.check_board_gems_pos(old_game_state, game_state)
        fill_reward = max(0, fill)
        reward += fill_reward * 0.2
        adjacent_reward = self.check_board_gems_adjacent_pos(old_game_state, game_state) 
        reward += adjacent_reward* 0.5
        collected_pieces_old = old_game_state.red_stones_collected + old_game_state.green_stones_collected
        collected_pieces = game_state.red_stones_collected + game_state.green_stones_collected
        gems_collected = collected_pieces - collected_pieces_old
        reward += collected_pieces_old*current_amount_moves
        reward += gems_collected*current_amount_moves*2

        
        return punishment - reward

    
    def a_star_search(self):
        self.grid_height = len(self.game.board)
        self.grid_width = len(self.game.board[0]) if self.grid_height > 0 else 0
        """A* Algorithm to solve the level"""
        initial_state = (copy.deepcopy(self.game),  [])  # (Game, Moves)
        queue = [(0, id(initial_state[0]), initial_state)] # deque([(0, id(initial_state[0]), initial_state)])# Priority Queue sorted by f = g + h
        visited = set()
        
        while queue:
            _, _, (game_state, g_moves) =  heapq.heappop(queue) #queue.popleft()
            # Verifica se o estado já foi visitado
            state_key = self.state_to_tuple(game_state, g_moves)
            if state_key in visited:
                continue
            visited.add(state_key)

            # If we collected all pieces, return the number of moves taken
            if game_state.check_level_complete() or game_state.game_won:
                return g_moves
            if game_state.game_over:
                continue

            possible_moves = self.get_all_possible_moves(game_state)
            # Não existem movimentos possíveis = Game over 
            if(possible_moves is None):
                continue
            
            # BFS itera sobre todos os movimentos possíveis
            for move in possible_moves:
                # Criar uma cópia do estado atual do jogo passado
                game_copy = copy.deepcopy(game_state)
                block_index, x, y = move
                block = game_copy.available_blocks[block_index]
                # Executar o movimento
                cleared = game_copy.place_block(block, x, y)
                game_copy.available_blocks[block_index] = None
                if game_copy.all_blocks_used():
                    game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()

                # Adicionar movimento à lista de moves executados
                new_g_moves = g_moves + [move]

                if game_copy.check_level_complete() or game_copy.game_won:
                    return new_g_moves
                if game_copy.game_over:
                    continue
                
                g = len(new_g_moves)
                h = self.heuristic(game_copy, game_state, cleared, len(new_g_moves))
                f = g + h  # f(n) = g(n) + h(n)
                # Assign a unique ID to the new state
                state_id = id(game_copy)
                if h < 0.4:
                    heapq.heappush(queue, (f, state_id, (game_copy, new_g_moves)))
        return None # If no solution is found
    
    
    def state_to_tuple(self, game_state, moves):
        """Convert state to a hashable format for tracking visited states"""
        board_tuple = tuple(tuple(row) for row in game_state.board)
        moves_tuple = tuple( move for move in moves )
        return (board_tuple, moves_tuple)



            
