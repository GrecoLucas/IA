from enum import Enum

class PlayerType(Enum):
    HUMAN = 1
    BOT = 2

class MenuState(Enum):
    ACTIVE = 1
    GAME_START = 2
    GAME_START_INF = 4
    EXIT = 3
    CHOOSE_ALGORITHM = 6

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
        self.selected_index = 0
        self.player_type = PlayerType.HUMAN
        self.state = MenuState.ACTIVE
        self.initialize_menu_items()
        self.bot_type = None

    def initialize_menu_items(self):
        """Define as opções do menu com base no estado atual."""
        if self.state == MenuState.ACTIVE:
            self.items = [
                MenuItem("Jogador Humano", self.set_player_human, PlayerType.HUMAN),
                MenuItem("Bot Automático", self.set_player_bot, PlayerType.BOT),
                MenuItem("Iniciar Jogo", self.start_game, None),
                MenuItem("Sair", self.exit_game, None),
            ]
        elif self.state == MenuState.CHOOSE_ALGORITHM:
            self.items = [
                MenuItem("Bot Random", self.set_bot_algorithm_random, "random"),
                MenuItem("Bot Otimizado", self.set_bot_algorithm_optimal, "optimal"),
                MenuItem("Gonçalo é o maior", self.set_bot_algorithm_random, None),
                MenuItem("Voltar", self.back_to_main_menu, None), 
            ]
        self.selected_index = 0  
        if self.items: 
            self.items[0].selected = True

    def set_player_human(self):
        self.player_type = PlayerType.HUMAN
        return False

    def set_player_bot(self):
        self.player_type = PlayerType.BOT
        self.state = MenuState.CHOOSE_ALGORITHM
        self.initialize_menu_items() 
        return False

    def set_bot_algorithm_random(self):
        self.bot_type = "random"
        self.state = MenuState.ACTIVE
        self.initialize_menu_items() 
        return False

    def set_bot_algorithm_optimal(self):
        self.bot_type = "optimal"
        self.state = MenuState.ACTIVE
        self.initialize_menu_items() 
        return False

    def back_to_main_menu(self):
        """Retorna ao menu principal."""
        self.state = MenuState.ACTIVE
        self.initialize_menu_items()
        return False


    def start_game(self):
        self.state = MenuState.GAME_START
        return True

    def start_game_infinit(self):
        self.state = MenuState.GAME_START_INF
        return True

    def exit_game(self):
        self.state = MenuState.EXIT
        return True

    def move_selection(self, direction):
        if not self.items: 
            return

        self.items[self.selected_index].selected = False
        if direction > 0:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        else:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        self.items[self.selected_index].selected = True

    def select_current(self):
        if not self.items: # Evita erros
            return False
        current_item = self.items[self.selected_index]
        if current_item.action:
            return current_item.action()
        return False

    def get_player_type(self):
        return self.player_type

    def get_bot_type(self):
        return self.bot_type

    def get_state(self):
        return self.state

    def get_selected_index(self):
        return self.selected_index

    def get_bot_name(self):
        """Retorna o nome do bot selecionado ou 'None'."""
        if self.bot_type:
            return self.bot_type
        return None
