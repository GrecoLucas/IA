# Projeto de IA
## Wood Block Puzzle

Um jogo de puzzle de blocos de madeira, onde você deve encaixar peças no tabuleiro.

## Como jogar
- Arraste e solte os blocos de madeira no tabuleiro
- Colete pedras verdes e/ou vermelhas para passar de nível 
- Complete linhas ou colunas inteiras para removê-las e ganhar pontos
- O jogo termina quando nenhum bloco disponível puder ser colocado no tabuleiro


## Instalação e execução
```
    sudo apt install python3-pygame #para instalar a depencia principal
    python3 game.py # correr o jogo
```

## Estrutura do Codigo

### `constants.py`
Define as constantes globais do jogo:
- Dimensões da tela e do tabuleiro
- Tamanho da grade
- Esquema de cores (madeira, pedras e elementos da interface)
- Configurações visuais

### `shapes.py`
Define os diferentes blocos que o jogador pode usar:
- Cada bloco é representado por uma matriz 2D usando "X" para partes sólidas e espaços vazios
- Blocos incluem formas como L, J, T invertido, linhas horizontais/verticais e blocos de canto
- Cada forma tem um nome único utilizado para identificação na sequência de jogo


### `levels.py`
Contém a configuração dos níveis do jogo:
- Cada nível especifica:
  - Número de pedras verdes e vermelhas necessárias para avançar
  - Sequência de blocos que serão disponibilizados ao jogador
  - Layout inicial do tabuleiro (blocos fixos, pedras coloridas e espaços vazios)
- O código de célula segue a convenção: 0=vazio, 1=madeira, 2=pedra verde, 3=pedra vermelha



### `game.py`
Implementa a lógica principal e a interface do jogo, organizado em três classes principais:

#### Classe `Block`
Responsável pela representação e renderização dos blocos:
- **Atributos:** forma, cor, dimensões, posição e offset para arrastar
- **Métodos:**
  - `__init__(shape_name)`: Inicializa um bloco, opcionalmente com forma específica
  - `draw(x, y)`: Renderiza o bloco na tela com efeitos visuais de textura

#### Classe `Level`
Encapsula as informações específicas de cada nível:
- **Atributos:** número do nível, objetivos (pedras a coletar), grade inicial, sequência de blocos

#### Classe `Game`
Gerencia a lógica central do jogo e a interface:
- **Atributos:**
  - Estado do tabuleiro e tipos de células
  - Blocos disponíveis e selecionados
  - Pontuação e progresso
  - Estado do jogo (em andamento, ganho, perdido)
- **Métodos principais:**
  - `load_level(level_index)`: Carrega o layout e objetivos do nível especificado
  - `get_next_blocks_from_sequence()`: Fornece o próximo bloco da sequência predefinida
  - `draw_board()`: Renderiza o tabuleiro, blocos, interface e informações do jogo
  - `is_valid_position(block, x, y)`: Verifica se um bloco pode ser colocado em determinada posição
  - `place_block(block, x, y)`: Posiciona um bloco no tabuleiro e processa suas consequências
  - `clear_rows()` e `clear_cols()`: Detectam e removem linhas/colunas completas
  - `check_game_over()`: Verifica se ainda existem movimentos válidos
  - `reset()`: Reinicia o jogo para seu estado inicial


#### Função `main()`
Inicializa o jogo e implementa o loop principal:
- Processa eventos de entrada (mouse, teclado)
- Gerencia o ciclo de arrastar e soltar blocos
- Atualiza o estado do jogo e a renderização
- Mantém o controle do tempo de quadro (FPS)
