# Projeto de IA - Wood Block Puzzle

Um jogo de puzzle de blocos de madeira, onde você deve encaixar peças no tabuleiro para completar linhas e colunas.

## Como jogar
- Arraste e solte os blocos de madeira no tabuleiro
- Colete pedras verdes e/ou vermelhas para passar de nível 
- Complete linhas ou colunas inteiras para removê-las e ganhar pontos
- O jogo termina quando nenhum bloco disponível puder ser colocado no tabuleiro

## Instalação e execução
```bash
# Instalar dependências
sudo apt install python3-pygame  # para instalar a biblioteca principal
pip install Pillow               # para suporte a animações GIF no menu

# Executar o jogo
python3 main.py
```

## Estrutura do Código (MVC)

### Model
#### Block
Define a classe Block que representa os blocos do jogo:
- **Atributos**: forma, cor, dimensões, posição e offset para arrastar
- **Métodos**: funcionalidades para obter as células ocupadas pelo bloco

#### Level
Encapsula as informações específicas de cada nível:
- **Atributos**: número do nível, objetivos (pedras a coletar), grade inicial, sequência de blocos
- **Métodos**: gerenciamento da sequência de blocos e verificação de conclusão de objetivos

#### Menu
Gerencia o estado do menu e as escolhas do jogador:
- Definição de tipos de jogador (humano/bot) e estados do menu
- Opções selecionáveis e ações correspondentes

#### Game
Implementa a lógica principal do jogo e gerencia o estado atual.

### View
#### Block_view
Renderização visual dos blocos no tabuleiro.

#### Game_view
Interface principal do jogo e renderização do tabuleiro.

#### Menu_view
Renderização dos elementos de menu e feedbacks visuais.

#### Level_view
Visualização de informações específicas do nível atual.

### Controller
#### Game_controller
Controle das interações do usuário durante o jogo.

#### Menu_controller
Gerenciamento das interações do usuário nos menus.

### Auxiliar
#### Constants
Definições de constantes utilizadas no jogo.

#### Shapes
Definições das formas dos blocos disponíveis.

#### Levels
Configurações dos diferentes níveis do jogo.

#### Main
Ponto de entrada da aplicação que inicializa e coordena os componentes.