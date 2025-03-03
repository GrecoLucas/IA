import random
import pygame
import sys
from shapes import SHAPES
from levels import LEVEL
from constants import *

# Inicializar o Pygame
pygame.init()

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wood Block - Puzzle Games")


class Block:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(WOOD_COLORS)
        self.rows = len(self.shape)
        self.cols = len(self.shape[0])
        self.x = random.randint(0, GRID_WIDTH - self.cols)
        self.y = 0
        self.selected = False
        self.offset_x = 0
        self.offset_y = 0
    
    def draw(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
            
        for i in range(self.rows):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] != " ":
                    rect = pygame.Rect(
                        BOARD_X + (x + j) * GRID_SIZE, 
                        BOARD_Y + (y + i) * GRID_SIZE, 
                        GRID_SIZE, GRID_SIZE
                    )
                    
                    # Desenhar o bloco de madeira com textura
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, (self.color[0] - 20, self.color[1] - 20, self.color[2] - 20), rect, 1)
                    
                    # Adicionar linhas de "madeira" para textura
                    for line in range(1, 3):
                        y_pos = rect.top + line * rect.height // 3
                        pygame.draw.line(
                            screen, 
                            (self.color[0] - 10, self.color[1] - 10, self.color[2] - 10),
                            (rect.left, y_pos),
                            (rect.right, y_pos),
                            1
                        )

class Game:
    def __init__(self):
        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.available_blocks = [Block() for _ in range(3)]
        self.block_positions = [
            (SCREEN_WIDTH // 4 - GRID_SIZE * 2, SCREEN_HEIGHT - 150),
            (SCREEN_WIDTH // 2 - GRID_SIZE * 2, SCREEN_HEIGHT - 150),
            (3 * SCREEN_WIDTH // 4 - GRID_SIZE * 2, SCREEN_HEIGHT - 150)
        ]
        self.selected_block = None
        self.score = 0
        self.green_stones_collected = 0
        self.level = 0  # Iniciar no nível 0 (primeiro nível)
        self.game_over = False
        self.game_won = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.load_level(0)  # Carregar o primeiro nível
    
    def load_level(self, level_index):
        if level_index < len(LEVEL):
            level_data = LEVEL[level_index]
            level_num = level_data[0]
            level_grid = level_data[1]
            
            # Reiniciar o tabuleiro
            self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            self.board_types = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            
            # Carregar a configuração do nível
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    cell_type = level_grid[y][x]
                    self.board_types[y][x] = cell_type
                    
                    if cell_type == 1:  # Bloco de madeira normal
                        self.board[y][x] = WOOD_MEDIUM
                    elif cell_type == 2:  # Pedra verde (objetivo)
                        self.board[y][x] = GREEN_POINT
                    elif cell_type == 3:  # Pedra vermelha (pontos extras)
                        self.board[y][x] = RED_POINT
            
            self.level = int(level_num)
            self.green_stones_collected = 0
            self.available_blocks = [Block() for _ in range(3)]
        else:
            # Se não houver mais níveis, o jogador venceu o jogo
            self.game_won = True
    
    def draw_board(self):
        # Desenhar fundo
        screen.fill(BACKGROUND_COLOR)
        
        # Desenhar título
        title = self.title_font.render(f"Wood Block Puzzle - Nível {self.level}", True, WOOD_DARK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
        
        # Desenhar a grade
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT)
        pygame.draw.rect(screen, WHITE, board_rect)
        pygame.draw.rect(screen, WOOD_DARK, board_rect, 2)
        
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
                    pygame.draw.rect(screen, color, rect)
                    
                    # Adicionar borda
                    if color == GREEN_POINT:
                        pygame.draw.rect(screen, (0, 150, 0), rect, 2)
                    elif color == RED_POINT:
                        pygame.draw.rect(screen, (150, 0, 0), rect, 2)
                    else:
                        pygame.draw.rect(screen, (color[0] - 20, color[1] - 20, color[2] - 20), rect, 1)
                        
                        # Linhas de textura para blocos de madeira
                        for line in range(1, 3):
                            y_pos = rect.top + line * rect.height // 3
                            pygame.draw.line(
                                screen, 
                                (color[0] - 10, color[1] - 10, color[2] - 10),
                                (rect.left, y_pos),
                                (rect.right, y_pos),
                                1
                            )
        
        # Desenhar blocos disponíveis
        for i, block in enumerate(self.available_blocks):
            if block:
                # Desenhar área de seleção
                selection_rect = pygame.Rect(
                    self.block_positions[i][0] - 10, 
                    self.block_positions[i][1] - 10,
                    block.cols * GRID_SIZE + 20,
                    block.rows * GRID_SIZE + 20
                )
                pygame.draw.rect(screen, (240, 240, 240), selection_rect, border_radius=10)
                pygame.draw.rect(screen, WOOD_DARK, selection_rect, 2, border_radius=10)
                
                # Desenhar o bloco na posição adequada
                for row in range(block.rows):
                    for col in range(len(block.shape[row])):
                        if block.shape[row][col] != " ":
                            rect = pygame.Rect(
                                self.block_positions[i][0] + col * GRID_SIZE,
                                self.block_positions[i][1] + row * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE
                            )
                            pygame.draw.rect(screen, block.color, rect)
                            pygame.draw.rect(screen, (block.color[0] - 20, block.color[1] - 20, block.color[2] - 20), rect, 1)
                            
                            # Linhas de textura
                            for line in range(1, 3):
                                y_pos = rect.top + line * rect.height // 3
                                pygame.draw.line(
                                    screen, 
                                    (block.color[0] - 10, block.color[1] - 10, block.color[2] - 10),
                                    (rect.left, y_pos),
                                    (rect.right, y_pos),
                                    1
                                )
        
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
            
            # Desenhar o bloco na posição do mouse com transparência
            for row in range(self.selected_block.rows):
                for col in range(len(self.selected_block.shape[row])):
                    if self.selected_block.shape[row][col] != " ":
                        rect = pygame.Rect(
                            BOARD_X + (grid_x + col) * GRID_SIZE,
                            BOARD_Y + (grid_y + row) * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE
                        )
                        if valid_position:
                            color = self.selected_block.color
                        else:
                            color = (255, 100, 100)  # Vermelho para posição inválida
                            
                        pygame.draw.rect(screen, color, rect, 0)
                        pygame.draw.rect(screen, (color[0] - 20, color[1] - 20, color[2] - 20), rect, 1)
        
        # Informações do jogo
        score_text = self.font.render(f"Pontuação: {self.score}", True, WOOD_DARK)
        level_text = self.font.render(f"Nível: {self.level}", True, WOOD_DARK)
        
        # Mostrar objetivo do nível
        if self.level == 1:
            objective_text = self.font.render(f"Objetivo: Colete 5 ou mais pedras verdes ({self.green_stones_collected}/5)", True, GREEN_POINT)
            screen.blit(objective_text, (20, SCREEN_HEIGHT - 50))
        
        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (SCREEN_WIDTH - 120, 20))
        
        # Exibir telas de game over ou vitória
        if self.game_over:
            game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            game_over_surface.fill((0, 0, 0, 180))
            screen.blit(game_over_surface, (0, 0))
            
            gameover_text = self.title_font.render("GAME OVER", True, WHITE)
            score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)
            restart_text = self.font.render("Pressione R para reiniciar", True, WHITE)
            
            screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        
        elif self.game_won:
            win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            win_surface.fill((0, 0, 0, 180))
            screen.blit(win_surface, (0, 0))
            
            win_text = self.title_font.render("PARABÉNS! VOCÊ VENCEU!", True, WHITE)
            score_text = self.font.render(f"Pontuação Final: {self.score}", True, WHITE)
            restart_text = self.font.render("Pressione R para jogar novamente", True, WHITE)
            
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    def is_valid_position(self, block, x, y):
        if x < 0 or y < 0:
            return False
            
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if block.shape[row][col] != " ":
                    # Verificar se está dentro dos limites do tabuleiro
                    if y + row >= GRID_HEIGHT or x + col >= GRID_WIDTH:
                        return False
                    # Verificar se a célula já está ocupada
                    if self.board[y + row][x + col]:
                        return False
        return True
    
    def place_block(self, block, x, y):
        green_stones_before = self.green_stones_collected
        
        # Colocar o bloco no tabuleiro
        for row in range(block.rows):
            for col in range(len(block.shape[row])):
                if block.shape[row][col] != " ":
                    # Verificar se há uma pedra verde na posição
                    if self.board_types[y + row][x + col] == 2:
                        # Coletou uma pedra verde
                        self.green_stones_collected += 1
                        self.score += 50  # Pontos extras por coletar pedra verde
                    
                    # Verificar se há uma pedra vermelha na posição
                    elif self.board_types[y + row][x + col] == 3:
                        self.score += 30  # Pontos extras por coletar pedra vermelha
                    
                    # Remover o tipo de bloco da grade de tipos
                    self.board_types[y + row][x + col] = 0
                    
                    # Colocar o bloco de madeira no tabuleiro
                    self.board[y + row][x + col] = block.color
        
        # Verificar e limpar linhas/colunas completas
        rows_cleared = self.clear_rows()
        cols_cleared = self.clear_cols()
        
        # Calcular pontuação
        cleared = rows_cleared + cols_cleared
        if cleared > 0:
            self.score += cleared * 10
        
        # Verificar se passou de nível (coletou 5 ou mais pedras verdes)
        if self.level == 1 and self.green_stones_collected >= 5 and green_stones_before < 5:
            self.load_level(self.level)  # Passar para o próximo nível (ou mostrar tela de vitória se não houver mais)
    
    def clear_rows(self):
        rows_cleared = 0
        for y in range(GRID_HEIGHT):
            # Verificar se a linha está completa (todos os espaços têm blocos de madeira)
            if all(self.board[y][x] is not None for x in range(GRID_WIDTH)):
                # Verificar se há pedras verdes na linha antes de removê-la
                for x in range(GRID_WIDTH):
                    if self.board_types[y][x] == 2:  # Se houver pedra verde
                        self.green_stones_collected += 1
                        self.score += 50  # Pontos extras por coletar pedra verde
                    elif self.board_types[y][x] == 3:  # Se houver pedra vermelha
                        self.score += 30  # Pontos extras por coletar pedra vermelha
                
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
                        self.score += 50  # Pontos extras por coletar pedra verde
                    elif self.board_types[y][x] == 3:  # Se houver pedra vermelha
                        self.score += 30  # Pontos extras por coletar pedra vermelha
                
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
    
    def reset(self):
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
                if event.button == 1:  # Botão esquerdo
                    mouse_x, mouse_y = event.pos
                    
                    # Verificar se clicou em algum bloco disponível
                    for i, block in enumerate(game.available_blocks):
                        if not block:  # Pular se o bloco já foi usado
                            continue
                            
                        block_rect = pygame.Rect(
                            game.block_positions[i][0] - 10, 
                            game.block_positions[i][1] - 10,
                            block.cols * GRID_SIZE + 20,
                            block.rows * GRID_SIZE + 20
                        )
                        
                        if block_rect.collidepoint(mouse_x, mouse_y):
                            # Calcular offset do clique em relação ao bloco
                            col_clicked = (mouse_x - game.block_positions[i][0]) // GRID_SIZE
                            row_clicked = (mouse_y - game.block_positions[i][1]) // GRID_SIZE
                            
                            # Verificar se clicou em uma parte do bloco
                            if (0 <= row_clicked < block.rows and 
                                0 <= col_clicked < len(block.shape[row_clicked]) and 
                                block.shape[row_clicked][col_clicked] != " "):
                                
                                game.selected_block = block
                                game.selected_block.offset_x = col_clicked
                                game.selected_block.offset_y = row_clicked
                                dragging = True
                                show_tutorial = False
                                break
            
            elif event.type == pygame.MOUSEBUTTONUP:
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
                            # Encontrar o índice do bloco selecionado
                            for i, block in enumerate(game.available_blocks):
                                if block is game.selected_block:
                                    game.place_block(game.selected_block, grid_x, grid_y)
                                    game.available_blocks[i] = None
                                    break
                                    
                            # Verificar se todos os blocos foram usados
                            if all(block is None for block in game.available_blocks):
                                game.available_blocks = [Block() for _ in range(3)]
                            
                            # Verificar se o jogador atingiu o objetivo do nível
                            if game.level == 1 and game.green_stones_collected >= 5:
                                game.game_won = True
                            
                            # Verificar se o jogo acabou (sem movimentos possíveis)
                            elif game.check_game_over():
                                game.game_over = True
                    
                    game.selected_block = None
        
        # Atualizar o jogo
        game.draw_board()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
