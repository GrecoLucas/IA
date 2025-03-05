import random
import pygame
import sys
from model.block import Block
from shapes import SHAPES
from levels import LEVEL_MAP, LEVELS
from constants import *
from view.block_view import BlockView

# Inicializar o Pygame
pygame.init()

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wood Block - Puzzle Games")


class Level:
    def __init__(self, level_num, green_blocks, red_blocks, grid, sequence):
        self.level_num = level_num
        self.grid = grid
        self.green_blocks = green_blocks # para coletar
        self.red_blocks = red_blocks   # para coletar 
        self.sequence = sequence
        self.current_block = None

class Game:
    def __init__(self):
        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.block_positions = [
            (SCREEN_WIDTH // 4 - GRID_SIZE * 2, SCREEN_HEIGHT - 150),
            (SCREEN_WIDTH // 2 - GRID_SIZE * 2, SCREEN_HEIGHT - 150),
            (3 * SCREEN_WIDTH // 4 - GRID_SIZE * 2, SCREEN_HEIGHT - 150)
        ]
        self.selected_block = None
        self.green_stones_collected = 0
        self.red_stones_collected = 0
        self.green_stones_to_collect = 0
        self.red_stones_to_collect = 0
        self.current_level = None
        self.level_num = 0
        self.sequence_index = 0 
        self.game_over = False
        self.game_won = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.load_level(0)
    

    def load_level(self, level_num):
        # Verifica se o nível existe no mapeamento
        if level_num in LEVEL_MAP:
            level_data = LEVEL_MAP[level_num]

            # Criar objeto Level
            self.current_level = Level(
                level_num=level_data.level_num,
                green_blocks=level_data.green_goal,
                red_blocks=level_data.red_goal, 
                grid=level_data.grid,
                sequence=level_data.sequence
            )

            # Reiniciar o tabuleiro
            self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

            # Carregar a configuração do nível do grid
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if y < len(level_data.grid) and x < len(level_data.grid[y]):
                        cell_type = level_data.grid[y][x]
                        self.board_types[y][x] = cell_type

                        if cell_type == 1:  # Bloco de madeira normal
                            self.board[y][x] = WOOD_MEDIUM
                        elif cell_type == 2:  # Pedra verde (objetivo)
                            self.board[y][x] = GREEN_POINT
                        elif cell_type == 3:  # Pedra vermelha (pontos extras)
                            self.board[y][x] = RED_POINT

            # Inicializar objetivos do nível
            self.level_num = level_data.level_num
            self.green_stones_collected = 0
            self.red_stones_collected = 0
            self.green_stones_to_collect = level_data.green_goal
            self.red_stones_to_collect = level_data.red_goal
            self.sequence_index = 0

            # Criar os primeiros blocos baseados na sequência
            self.available_blocks = self.get_next_blocks_from_sequence()
        else:
            # Se o nível não existe, verificar se terminamos todos os níveis
            max_level = max(level.level_num for level in LEVELS)
            if level_num > max_level:
                # Se sim, declarar vitória
                self.game_won = True
            else:
                # Se não, tente carregar o nível 0 (tutorial)
                if level_num != 0:
                    print(f"Nível {level_num} não encontrado. Carregando nível 0.")
                    self.load_level(0)
                else:
                    # Se mesmo o nível 0 não existe, temos um problema
                    print("Erro: Nenhum nível definido no jogo.")
                    self.game_over = True

    def get_next_blocks_from_sequence(self):
        if not self.current_level or not self.current_level.sequence:
            print("Sem sequência definida, usando bloco aleatório")
            return [Block(), None, None]  # Apenas um bloco
        
        blocks = [None, None, None]  # Inicializa com três posições vazias
        
        # Obter o próximo tipo de bloco da sequência
        if self.sequence_index < len(self.current_level.sequence):
            shape_name = self.current_level.sequence[self.sequence_index]
            print(f"Próximo bloco da sequência: {shape_name}")
            
            # Verificar se o nome do bloco existe em SHAPES
            if shape_name in SHAPES:
                self.sequence_index = (self.sequence_index + 1) % len(self.current_level.sequence)
                blocks[0] = Block(shape_name)  # Coloca apenas na primeira posição
            else:
                print(f"ERRO: Forma '{shape_name}' não encontrada em SHAPES!")
                # Usar um bloco aleatório se o nome não existir
                blocks[0] = Block()
        else:
            # Se a sequência acabou, criar um bloco aleatório
            blocks[0] = Block()
    
        return blocks
    

    def draw_board(self):
        # Desenhar fundo
        screen.fill(BACKGROUND_COLOR)

        # Desenhar título
        title = self.title_font.render(f"Wood Block Puzzle - Nível {self.level_num}", True, WOOD_DARK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))

        # Desenhar a grade
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT)
        pygame.draw.rect(screen, WHITE, board_rect)
        pygame.draw.rect(screen, WOOD_DARK, board_rect, 2)

        # Draw grid lines
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(
                screen, GRID_COLOR, 
                (BOARD_X + i * GRID_SIZE, BOARD_Y), 
                (BOARD_X + i * GRID_SIZE, BOARD_Y + GRID_HEIGHT * GRID_SIZE),
                1
            )
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                screen, GRID_COLOR, 
                (BOARD_X, BOARD_Y + i * GRID_SIZE), 
                (BOARD_X + GRID_WIDTH * GRID_SIZE, BOARD_Y + i * GRID_SIZE),
                1
            )

        # Desenhar os blocos colocados no tabuleiro
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    color = self.board[y][x]
                    rect = pygame.Rect(
                        BOARD_X + x * GRID_SIZE, 
                        BOARD_Y + y * GRID_SIZE, 
                        GRID_SIZE, GRID_SIZE
                    )
                    
                    # Adicionar borda especial para pedras verdes e vermelhas
                    if color == GREEN_POINT:
                        pygame.draw.rect(screen, color, rect)
                        pygame.draw.rect(screen, (0, 150, 0), rect, 2)
                    elif color == RED_POINT:
                        pygame.draw.rect(screen, color, rect)
                        pygame.draw.rect(screen, (150, 0, 0), rect, 2)
                    else:
                        # Use o BlockView para desenhar blocos de madeira
                        BlockView.draw_wood_block(screen, color, rect)

        # Desenhar blocos disponíveis (apenas o primeiro)
        if self.available_blocks[0]:  
            block = self.available_blocks[0]
            # Centralizar o bloco na tela na parte inferior
            block_x = SCREEN_WIDTH // 2 - (block.cols * GRID_SIZE) // 2
            block_y = SCREEN_HEIGHT - 200
            
            # Atualizar a posição do bloco para desenho e interação
            self.block_positions[0] = (block_x, block_y)
            
            # Usar o BlockView para desenhar o bloco
            BlockView.draw_available_block(screen, block, (block_x, block_y), self.font)
        
        # Desenhar bloco selecionado seguindo o mouse
        if self.selected_block:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = (mouse_x - BOARD_X) // GRID_SIZE
            grid_y = (mouse_y - BOARD_Y) // GRID_SIZE
            
            # Ajustar para o offset do bloco selecionado
            grid_x -= self.selected_block.offset_x
            grid_y -= self.selected_block.offset_y
            
            # Verificar se a posição é válida
            valid_position = self.is_valid_position(self.selected_block, grid_x, grid_y)
            
            # Usar o BlockView para desenhar o bloco na posição do mouse
            BlockView.draw_block(screen, self.selected_block, grid_x, grid_y, valid_position)
        
        # Desenhar objetivos
        objective_text = self.font.render(
            f"Pedras verdes coletadas: {self.green_stones_collected}/{self.green_stones_to_collect}", 
            True, WOOD_DARK
        )
        screen.blit(objective_text, (20, SCREEN_HEIGHT - 50))
        
        objective_text = self.font.render(
            f"Pedras vermelhas coletadas: {self.red_stones_collected}/{self.red_stones_to_collect}", 
            True, WOOD_DARK
        )
        screen.blit(objective_text, (20, SCREEN_HEIGHT - 30))
        
        # Exibir telas de game over ou vitória
        if self.game_over:
            game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            game_over_surface.fill((0, 0, 0, 180))
            screen.blit(game_over_surface, (0, 0))
            
            gameover_text = self.title_font.render("GAME OVER", True, WHITE)
            restart_text = self.font.render("Pressione R para reiniciar", True, WHITE)
            
            screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        
        elif self.game_won:
            win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            win_surface.fill((0, 0, 0, 180))
            screen.blit(win_surface, (0, 0))
            
            win_text = self.title_font.render("PARABÉNS! VOCÊ VENCEU!", True, WHITE)
            restart_text = self.font.render("Pressione R para jogar novamente", True, WHITE)
            
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    
    def is_valid_position(self, block, x, y):
        if x < 0 or y < 0:
            return False
            
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if col < len(block.shape[row]) and block.shape[row][col] == "X":
                    # Verificar se está dentro dos limites do tabuleiro
                    if y + row >= GRID_HEIGHT or x + col >= GRID_WIDTH:
                        return False
                    # Verificar se a célula já está ocupada
                    if self.board[y + row][x + col]:
                        return False
        return True
    
    def place_block(self, block, x, y):
        
        # Colocar o bloco no tabuleiro
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if col < len(block.shape[row]) and block.shape[row][col] == "X":
                    # Verificar se há uma pedra verde na posição
                    if self.board_types[y + row][x + col] == 2:
                        # Coletou uma pedra verde
                        self.green_stones_collected += 1
                    
                    # Verificar se há uma pedra vermelha na posição
                    elif self.board_types[y + row][x + col] == 3:
                        self.red_stones_collected += 1
                    
                    # Remover o tipo de bloco da grade de tipos
                    self.board_types[y + row][x + col] = 0
                    
                    # Colocar o bloco de madeira no tabuleiro
                    self.board[y + row][x + col] = block.color
        
        # Verificar e limpar linhas/colunas completas
        rows_cleared = self.clear_rows()
        cols_cleared = self.clear_cols()

    def clear_rows(self):
        rows_cleared = 0
        for y in range(GRID_HEIGHT):
            # Verificar se a linha está completa (todos os espaços têm blocos de madeira)
            if all(self.board[y][x] is not None for x in range(GRID_WIDTH)):
                # Verificar se há pedras verdes na linha antes de removê-la
                for x in range(GRID_WIDTH):
                    if self.board_types[y][x] == 2:  # Se houver pedra verde
                        self.green_stones_collected += 1
                    elif self.board_types[y][x] == 3:  # Se houver pedra vermelha
                        self.red_stones_collected += 1
                
                # Limpar a linha (remover os blocos)
                for x in range(GRID_WIDTH):
                    self.board[y][x] = None
                    self.board_types[y][x] = 0
                rows_cleared += 1
                
                # Efeito visual para a linha sendo removida
                self.draw_board()
                pygame.display.flip()
                pygame.time.delay(100)  # Pequeno delay para o efeito visual
                
        return rows_cleared
    
    def clear_cols(self):
        cols_cleared = 0
        for x in range(GRID_WIDTH):
            # Verificar se a coluna está completa (todos os espaços têm blocos de madeira)
            if all(self.board[y][x] is not None for y in range(GRID_HEIGHT)):
                # Verificar se há pedras verdes na coluna antes de removê-la
                for y in range(GRID_HEIGHT):
                    if self.board_types[y][x] == 2:  # Se houver pedra verde
                        self.green_stones_collected += 1
                    elif self.board_types[y][x] == 3:  # Se houver pedra vermelha
                        self.red_stones_collected += 1                 
                # Limpar a coluna (remover os blocos)
                for y in range(GRID_HEIGHT):
                    self.board[y][x] = None
                    self.board_types[y][x] = 0
                cols_cleared += 1
                
                # Efeito visual para a coluna sendo removida
                self.draw_board()
                pygame.display.flip()
                pygame.time.delay(100)  # Pequeno delay para o efeito visual
                
        return cols_cleared
    
    def check_game_over(self):
        # Verificar se algum bloco disponível pode ser colocado no tabuleiro
        for block in self.available_blocks:
            if not block:  # Pular se o bloco já foi usado
                continue
                
            can_place = False
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.is_valid_position(block, x, y):
                        can_place = True
                        break
                if can_place:
                    break
            
            if can_place:
                return False  # Pelo menos um bloco pode ser colocado
        
        # Se nenhum bloco puder ser colocado, o jogo acabou
        return True
    
    def reset(self): # Reiniciar o jogo
        self.__init__()

def main():
    game = Game()
    clock = pygame.time.Clock()
    dragging = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game.game_over or game.game_won):
                    game.reset()
            
            if game.game_over or game.game_won:
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                               # No evento MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    mouse_x, mouse_y = event.pos
                    
                    # Verificar se clicou no bloco disponível (apenas o primeiro)
                    if game.available_blocks[0]:  # Verifica apenas o primeiro bloco
                        block = game.available_blocks[0]
                        block_rect = pygame.Rect(
                            game.block_positions[0][0] - 10, 
                            game.block_positions[0][1] - 10,
                            block.cols * GRID_SIZE + 20,
                            block.rows * GRID_SIZE + 20
                        )
                        
                        if block_rect.collidepoint(mouse_x, mouse_y):
                            # Calcular offset do clique em relação ao bloco
                            col_clicked = (mouse_x - game.block_positions[0][0]) // GRID_SIZE
                            row_clicked = (mouse_y - game.block_positions[0][1]) // GRID_SIZE
                            
                            # Verificar se clicou em uma parte do bloco
                            if (0 <= row_clicked < block.rows and 
                                0 <= col_clicked < len(block.shape[row_clicked]) and 
                                block.shape[row_clicked][col_clicked] == "X"):
                                
                                game.selected_block = block
                                game.selected_block.offset_x = col_clicked
                                game.selected_block.offset_y = row_clicked
                                dragging = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # No evento MOUSEBUTTONUP:
                if event.button == 1 and dragging:  # Botão esquerdo
                    dragging = False
                    mouse_x, mouse_y = event.pos
                    
                    if (BOARD_X <= mouse_x <= BOARD_X + GRID_WIDTH * GRID_SIZE and
                        BOARD_Y <= mouse_y <= BOARD_Y + GRID_HEIGHT * GRID_SIZE):
                        
                        grid_x = (mouse_x - BOARD_X) // GRID_SIZE
                        grid_y = (mouse_y - BOARD_Y) // GRID_SIZE
                        
                        # Ajustar para o offset do bloco selecionado
                        grid_x -= game.selected_block.offset_x
                        grid_y -= game.selected_block.offset_y
                        
                        # Tentar colocar o bloco
                        if game.is_valid_position(game.selected_block, grid_x, grid_y):
                            game.place_block(game.selected_block, grid_x, grid_y)
                            game.available_blocks[0] = None  # Marcar o bloco como usado

                            # Verificar se o jogador atingiu o objetivo do nível
                        if (game.green_stones_collected >= game.green_stones_to_collect and 
                            game.red_stones_collected >= game.red_stones_to_collect):
                            
                            # Encontrar o próximo nível
                            next_levels = [level.level_num for level in LEVELS if level.level_num > game.level_num]
                            if next_levels:
                                next_level = min(next_levels)
                                game.load_level(next_level)
                            else:
                                # Se não houver mais níveis, declarar vitória
                                game.game_won = True
                                                    # Verificar se o bloco foi usado para gerar novo bloco
                        elif game.available_blocks[0] is None:
                            game.available_blocks = game.get_next_blocks_from_sequence()
                        
                            # Verificar se o jogo acabou (sem movimentos possíveis)
                        if game.check_game_over():
                            game.game_over = True

                    game.selected_block = None
        
        # Atualizar o jogo
        game.draw_board()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
