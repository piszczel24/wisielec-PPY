import tkinter as tk
from tkinter import messagebox

import bcrypt
from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import sessionmaker, declarative_base

from game import Game
from playerdto import PlayerDto

SCREEN_WIDTH = 1960
SCREEN_HEIGHT = 1080
BG_COLOR = "#13a18b"
BUTTON_COLOR = "#64a18b"
BUTTON_FONT = ("Comic sans MS", 10)
FORM_BUTTON_FONT = ("Comic sans MS", 30)

Base = declarative_base()

engine = create_engine("postgresql://pycharm:pycharm@localhost:5432/postgres", echo=True)
Session = sessionmaker(bind=engine)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


class Player(Base):
    __tablename__ = "Player"

    id_player = Column("IdPlayer", Integer, primary_key=True)
    nickname = Column("Nickname", String)
    password = Column("Password", String)
    best_score = Column("BestScore", Integer)

    def __init__(self, id_player, nickname, password):
        self.id_player = id_player
        self.nickname = nickname
        self.password = password
        self.best_score = 0

    def add_win(self):
        self.best_score += 1


Base.metadata.create_all(bind=engine)


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
        player1 = PlayerDto(1, "Adam")
        player2 = PlayerDto(2, "Bartosz")

        game = Game(player1, player2)
        game.run()
        self.deiconify()

    def login_player(self) -> None:
        pass

    def register_player(self) -> None:
        self.withdraw()
        RegisterPlayer()
        self.deiconify()

    def show_stats(self) -> None:
        pass

    def show_options(self) -> None:
        pass

    def exit_app(self) -> None:
        self.destroy()


class RegisterPlayer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Rejestracja")

        window_width = 600
        window_height = 700
        x = (SCREEN_WIDTH - window_width) // 2
        y = (SCREEN_HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        title_label = tk.Label(self, text="REJESTRACJA", font=("Comic sans MS", 50), pady=30, bg=BG_COLOR)
        title_label.pack()

        nickname_label = tk.Label(self, text="LOGIN:", font=FORM_BUTTON_FONT, pady=10, bg=BG_COLOR)
        nickname_label.pack()

        nickname_entry = tk.Entry(self)
        nickname_entry.place(x=200, y=250, width=200, height=30)

        password_label = tk.Label(self, text="HASŁO:", font=FORM_BUTTON_FONT, pady=10, bg=BG_COLOR)
        password_label.place(x=220, y=300)

        password_entry = tk.Entry(self, show="*")
        password_entry.place(x=200, y=400, width=200, height=30)

        confirm_button = tk.Button(self, text="ZAREJESTRUJ", font=BUTTON_FONT,
                                   command=lambda: self.add_to_db(nickname_entry.get(), password_entry.get()), width=12,
                                   height=1, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        confirm_button.place(x=500, y=400)

    def add_to_db(self, nickname: str, password: str):
        session = Session()
        max_id = session.query(func.max(Player.id_player)).scalar()
        max_id = max_id or 0
        max_id = int(max_id)
        session.add(Player(max_id + 1, nickname, hash_password(password)))
        session.commit()
        self.destroy()


elo = StartWindow()
elo.mainloop()
