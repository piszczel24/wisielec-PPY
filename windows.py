import tkinter as tk
import tkinter.messagebox as messagebox

import bcrypt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base

import db_initialize
from db_initialize import Player
from game import Game

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
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


Base.metadata.create_all(bind=engine)


class StartWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.session = Session()
        self.title("Wisielec")

        db_initialize.db_initialize()
        window_width = 800
        window_height = 400
        x = (SCREEN_WIDTH - window_width) // 2
        y = (SCREEN_HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        self.logged_players: list[Player] = []

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

        exit_app_button = tk.Button(self, text="WYJDŹ", font=BUTTON_FONT, command=self.exit_app, width=12,
                                    height=1,
                                    bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        exit_app_button.pack(side=tk.LEFT, padx=10)

    def start_game(self) -> None:
        if len(self.logged_players) >= 2:
            self.withdraw()
            game = Game(self.session.merge(self.logged_players[0]), self.session.merge(self.logged_players[1]))
            game.run()
            self.deiconify()
        else:
            messagebox.showinfo("Błąd", "Za mało zalogowanych graczy!")

    def login_player(self) -> None:
        self.withdraw()
        LoginWindow(self)
        self.deiconify()

    def register_player(self) -> None:
        self.withdraw()
        RegisterWindow()
        self.deiconify()

    def show_stats(self) -> None:
        pass

    def show_options(self) -> None:
        pass

    def exit_app(self) -> None:
        self.destroy()
        self.quit()


class RegisterWindow(tk.Tk):
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
        confirm_button.place(x=250, y=500)

    def add_to_db(self, nickname: str, password: str) -> None:
        session = Session()
        max_id = session.query(func.max(Player.id_player)).scalar()
        max_id = max_id or 0
        max_id = int(max_id)
        session.add(Player(max_id + 1, nickname, hash_password(password)))
        session.commit()
        self.destroy()
        messagebox.showinfo("Rejestracja", "Zarejestrowano pomyślnie!")


class LoginWindow(tk.Tk):
    def __init__(self, master: StartWindow) -> None:
        super().__init__()
        self.title("Rejestracja")

        window_width = 600
        window_height = 700
        x = (SCREEN_WIDTH - window_width) // 2
        y = (SCREEN_HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        title_label = tk.Label(self, text="LOGOWANIE", font=("Comic sans MS", 50), pady=30, bg=BG_COLOR)
        title_label.pack()

        nickname_label = tk.Label(self, text="LOGIN:", font=FORM_BUTTON_FONT, pady=10, bg=BG_COLOR)
        nickname_label.pack()

        nickname_entry = tk.Entry(self)
        nickname_entry.place(x=200, y=250, width=200, height=30)

        password_label = tk.Label(self, text="HASŁO:", font=FORM_BUTTON_FONT, pady=10, bg=BG_COLOR)
        password_label.place(x=220, y=300)

        password_entry = tk.Entry(self, show="*")
        password_entry.place(x=200, y=400, width=200, height=30)

        confirm_button = tk.Button(self, text="ZALOGUJ", font=BUTTON_FONT,
                                   command=lambda: self.check_in_db(nickname_entry.get(), password_entry.get(), master),
                                   width=12, height=1, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        confirm_button.place(x=250, y=500)

    def check_in_db(self, nickname: str, password: str, master: StartWindow):
        session = Session()
        player = session.query(Player).filter_by(nickname=nickname).first()
        if player and verify_password(password, player.password):
            self.destroy()
            master.logged_players.append(player)
            messagebox.showinfo("Logowanie", "Zalogowano pomyślnie!")
        else:
            self.destroy()
            messagebox.showinfo("Logowanie", "Błędny login lub hasło!")
        session.commit()


class StatsWindow(tk.Tk):
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

        title_label = tk.Label(self, text="Statystyki graczy", font=("Comic sans MS", 20), pady=30, bg=BG_COLOR)
        title_label.pack()


elo = StartWindow()
elo.mainloop()
