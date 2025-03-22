from enum import Enum

class PlayerType(Enum):
    HUMAN = 1
    BOT = 2

class MenuState(Enum):
    ACTIVE = 1
    GAME_START = 2
    GAME_START_INF = 4
    EXIT = 3
    CHOOSE_BOT = 5

class MenuItem:
    def __init__(self, text, action=None, value=None):
        self.text = text
        self.action = action
        self.value = value
        self.selected = False
    
    def get_value(self):
        return self.value

class Menu:
    def __init__(self):
        self.items = []
        self.selected_index = 0
        self.player_type = PlayerType.HUMAN
        self.state = MenuState.ACTIVE
        self.initialize_menu_items()
        self.bot_type = None
    
    def initialize_menu_items(self):
        """Define opções de menu padrão"""
        self.items = [
            MenuItem("Jogador Humano", self.set_player_human, PlayerType.HUMAN),
            MenuItem("Bot Automático", self.set_player_bot, PlayerType.BOT),
            MenuItem("Iniciar Jogo", self.start_game, None),
            MenuItem("Sair", self.exit_game, None),
            MenuItem("Bot Random", self.set_bot_algorithm_random, "random"),
            MenuItem("Bot Otimizado", self.set_bot_algorithm_optimal, "optimal"), #"iterative"
            MenuItem("Bot Iterativo", self.set_bot_algorithm_iterative, "iterative"),
        ]
        # Define o primeiro item como selecionado inicialmente
        self.items[0].selected = True
    
    def set_player_human(self):
        """Define o tipo de jogador como humano"""
        self.player_type = PlayerType.HUMAN
        return False  # Não fechar o menu após esta ação
    
    def set_player_bot(self):
        """Define o tipo de jogador como bot"""
        self.player_type = PlayerType.BOT
        self.state = MenuState.CHOOSE_BOT
        return False  # Não fechar o menu após esta ação
    
    def set_bot_algorithm_random(self):
        """Define i tipo de algoritmo do bot"""
        self.bot_type = "random"
        
        return False
    
    def set_bot_algorithm_optimal(self):
        """Define i tipo de algoritmo do bot"""
        self.bot_type = "optimal"
        return False
    
    def set_bot_algorithm_iterative(self):
        """Define i tipo de algoritmo do bot"""
        self.bot_type = "iterative"
        return False
    
    def start_game(self):
        """Inicia o jogo com as configurações definidas"""
        self.state = MenuState.GAME_START
        
        return True  # Fechar o menu e iniciar o jogo
    
    def start_game_infinit(self):
        self.state = MenuState.GAME_START_INF
        return True

    def exit_game(self):
        """Sai do jogo"""
        self.state = MenuState.EXIT
        return True  # Fechar o menu e sair
    
    def move_selection(self, direction):
        """Move a seleção para cima ou para baixo"""
        # Desselecionar o item atual
        self.items[self.selected_index].selected = False
        
        # Mover a seleção
        if direction > 0:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        else:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        
        # Selecionar o novo item
        self.items[self.selected_index].selected = True
    
    def select_current(self):
        """Executa a ação do item selecionado"""
        current_item = self.items[self.selected_index]
        if current_item.action:
            return current_item.action()
        return False
    
    def get_player_type(self):
        """Retorna o tipo de jogador selecionado"""
        return self.player_type
    
    def get_bot_type(self):
        """Retorna o tipo de bot selecionado"""
        return self.bot_type
    
    def get_state(self):
        """Retorna o estado atual do menu"""
        return self.state
    
    def get_selected_index(self):
        """Retorna o índice do item selecionado"""
        return self.selected_index