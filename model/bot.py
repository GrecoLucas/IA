from constants import *
import copy
import random
from collections import deque

class Bot:
    def __init__(self, game, algorithm):
        self.game = game
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
        possible_moves = []
        
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
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
        possible_moves = []
    
        # Coletar todos os movimentos possíveis
        for block_index, block in enumerate(self.game.available_blocks):
            if block is None:
                continue
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
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
                        for sim_y in range(GRID_HEIGHT):
                            for sim_x in range(GRID_WIDTH):
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
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        
        if not possible_moves:
            self.__class__.bfa_cache[game_state_key] = None
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
                # Otimização: se encontramos um caminho curto, priorizamos ele
                if len(path) <= 10:  # Considere caminhos curtos 
                    self.__class__.bfa_cache[game_state_key] = path[0] if path else None
                    return path[0] if path else None
                continue  # Continue procurando outros caminhos possíveis
            
            # Se o jogo terminou sem vitória, pule
            if current_game.game_over:
                continue
            
            # Coletar todos os movimentos possíveis para o estado atual do jogo
            possible_moves = []
            for block_index, block in enumerate(current_game.available_blocks):
                if block is None:
                    continue
                for y in range(GRID_HEIGHT):
                    for x in range(GRID_WIDTH):
                        if current_game.is_valid_position(block, x, y):
                            possible_moves.append((block_index, x, y))
            
            if not possible_moves:
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
        
        # Selecione o melhor caminho (o mais curto) entre os caminhos vencedores
        best_move = None
        if winning_paths:
            shortest_path = min(winning_paths, key=len)
            if shortest_path:
                best_move = shortest_path[0]  # O primeiro movimento do caminho mais curto
        
        # Salve a solução no cache
        self.__class__.bfa_cache[game_state_key] = best_move
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
            x = random.randint(0,GRID_WIDTH-1)
            y = random.randint(0,GRID_HEIGHT-1)
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
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if game.is_valid_position(block, x, y):
                        possible_moves.append((block_index, x, y))
        # Não foi encontrado nenhum movimento possível
        if not possible_moves:
            return None
        
        return possible_moves

    # Iterative deepening search para encontrar o melhor movimento
    def iterative_deepening_search(self, max_depth):
        for depth in range(1, max_depth):
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
        # conjunto de movimentos atuais permitem ganhar o jogo
        if game.game_won:
            return move_seq
        # Nenhuma solução encontrada para a profundidade dada
        if depth == 0:
            return None
        
        possible_moves = self.get_all_possible_moves(game)
        # BFS itera sobre todos os movimentos possíveis 
        if(possible_moves is None):
            return None
        for move in possible_moves:
            # Criar uma cópia do estado atual do jogo passado
            game_copy = copy.deepcopy(game)
            
            block_index, x, y = move
            #print(f"index: {block_index}, x: {x}, y: {y}")
            block = game_copy.available_blocks[block_index]
            # Executar o movimento
            game_copy.place_block(block, x, y)
            game_copy.available_blocks[block_index] = None
            # Adicionar movimento à lista de moves executados
            new_move_seq = move_seq + [move]
            # Nível completo 
            if game_copy.check_level_complete():
                    #print(f"LEVEL {game_copy.level_num} COMPLETE!!!")
                    next_level = game_copy.get_next_level()
                    if next_level is not None:
                        game_copy.load_level(next_level)
                        # Evitar explorar outros movimentos que não completam o nível
                        result = self.recursive_depth_limited_search(game_copy, depth-1, new_move_seq )
                        return result
                    else:
                        game_copy.game_won = True
                        
            # Atualizar blocos disponíveis se necessário
            elif game_copy.all_blocks_used():
                game_copy.available_blocks = game_copy.get_next_blocks_from_sequence()
            result = self.recursive_depth_limited_search(game_copy, depth-1, new_move_seq )
            if result is not None:
                return result   # Sequência de movimentos válida encontrada
        # Não foi encontrada nenhuma sequência de movimentos válida para ganhar o jogo
        return None
            

            
