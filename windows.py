import tkinter as tk

from game import Game
from player import Player

SCREEN_WIDTH = 1960
SCREEN_HEIGHT = 1080
BG_COLOR = "#13a18b"
BUTTON_COLOR = "#64a18b"
BUTTON_FONT = ("Comic sans MS", 10)


class StartWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Wisielec")

        window_width = 800
        window_height = 400
        x = (SCREEN_WIDTH - window_width) // 2
        y = (SCREEN_HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        game_title = tk.Label(self, text="WISIELEC", font=("Comic sans MS", 50), pady=30, bg=BG_COLOR)
        game_title.pack()

        start_game_button = tk.Button(self, text="START", font=BUTTON_FONT, command=self.start_game, width=12, height=1,
                                      bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        start_game_button.pack(side=tk.LEFT, padx=22)

        login_button = tk.Button(self, text="LOGIN", font=BUTTON_FONT, command=self.login_player, width=12, height=1,
                                 bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        login_button.pack(side=tk.LEFT, padx=10)

        register_button = tk.Button(self, text="ZAREJESTRUJ", font=BUTTON_FONT, command=self.register_player, width=12,
                                    height=1, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        register_button.pack(side=tk.LEFT, padx=10)

        stats_button = tk.Button(self, text="STATYSTYKI", font=BUTTON_FONT, command=self.show_stats, width=12, height=1,
                                 bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        stats_button.pack(side=tk.LEFT, padx=10)

        options_button = tk.Button(self, text="OPCJE", font=BUTTON_FONT, command=self.show_stats, width=12,
                                   height=1, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        options_button.pack(side=tk.LEFT, padx=10)

        exit_app_button = tk.Button(self, text="EXIT", font=BUTTON_FONT, command=self.exit_app, width=12, height=1,
                                    bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        exit_app_button.pack(side=tk.LEFT, padx=10)

    def start_game(self) -> None:
        self.withdraw()
        player1 = Player(1, "Adam")
        player2 = Player(2, "Bartosz")

        game = Game(player1, player2)
        game.run()
        self.deiconify()

    def login_player(self) -> None:
        pass

    def register_player(self) -> None:
        pass

    def show_stats(self) -> None:
        pass

    def show_options(self) -> None:
        pass

    def exit_app(self) -> None:
        self.destroy()


elo = StartWindow()
elo.mainloop()
