"""Moduł zawiera klasy ze wszystkimi rodzajami okien w aplikacji.

Attributes:
    WIDTH (int): Szerokość okna gry.
    HEIGHT (int): Wysokość okna gry.
    BG_COLOR (str): Kolor tła w formacie heksadecymanym.
    BG_CBUTTON_COLOR OLOR (str): Kolor tła w formacie heksadecymanym.
    Base: Klasa będąca reprezentacją bazy deklaratywnej.
    engine (sqlalchemy.engine.Engine): Silnik bazy danych, łączący się z nią przez connection stringa.
    Session: Klasa reprezentująca sesję połączenia z bazą danych.

"""
import csv
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk, filedialog
import bcrypt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base
import db_initialize
from db_initialize import Player
from game import Game

WIDTH = 1960
HEIGHT = 1080
BG_COLOR = "#13a18b"
BUTTON_COLOR = "#64a18b"
BUTTON_FONT = ("Comic sans MS", 10)
FORM_BUTTON_FONT = ("Comic sans MS", 30)

Base = declarative_base()
engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)


def hash_password(password: str) -> str:
    """Funkcja hashuje hasło.

    Args:
        password: Hasło do shashowania.

    Returns:
        Shashowane hasło.

    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Sprawdza czy zwykłe hasło zgadza się z tym shashowanym.

    Args:
        password: Zwykłe hasło.
        hashed_password: Shashowane hasło.

    Returns:
        Prawda, jeżeli hasła się zgadzają. Fałsz w przeciwnym przypadku

    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


Base.metadata.create_all(bind=engine)


class StartWindow(tk.Tk):
    """Klasa reprezentuje ekran startowy aplikacji - memu główne.

    Attributes:
        session (sqlalchemy.orm.Session): Sesja połączenia do bazy danych.
        logged_players (list[Player]): Lista zalogowanych graczy.
        difficulty (int): Poziom trudności: 0 - klasyczny, 1 - hradcore.

    """

    def __init__(self) -> None:
        super().__init__()
        self.session = Session()
        self.title("Wisielec")

        db_initialize.db_initialize()
        window_width = 800
        window_height = 400
        x = (WIDTH - window_width) // 2
        y = (HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        self.logged_players = []

        self.difficulty = 0

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

        options_button = tk.Button(self, text="OPCJE", font=BUTTON_FONT, command=self.show_options, width=12,
                                   height=1, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        options_button.pack(side=tk.LEFT, padx=10)

        exit_app_button = tk.Button(self, text="WYJDŹ", font=BUTTON_FONT, command=self.exit_app, width=12,
                                    height=1,
                                    bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        exit_app_button.pack(side=tk.LEFT, padx=10)

    def start_game(self) -> None:
        """Odpala grę."""
        if len(self.logged_players) >= 2:
            self.withdraw()
            game = Game(self.session.merge(self.logged_players[0]), self.session.merge(self.logged_players[1]))
            game.difficulty = self.difficulty
            game.run()
            self.deiconify()
        else:
            messagebox.showinfo("Błąd", "Za mało zalogowanych graczy!")

    def login_player(self) -> None:
        """Wyświetla ekran logowania."""
        self.withdraw()
        LoginWindow(self)
        self.deiconify()

    def register_player(self) -> None:
        """Wyświetla ekran rejestracji."""
        self.withdraw()
        RegisterWindow()
        self.deiconify()

    def show_stats(self) -> None:
        """Wyświetla ekran statystyk."""
        self.withdraw()
        StatsWindow()
        self.deiconify()

    def show_options(self) -> None:
        """Wyświetla ekran opcji."""
        self.withdraw()
        OptionsWindow(self)
        self.deiconify()

    def exit_app(self) -> None:
        """Zamyka aplikację."""
        self.destroy()
        self.quit()


class RegisterWindow(tk.Tk):
    """Klasa reprezentuje ekran rejestracji graczy."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Rejestracja")

        window_width = 600
        window_height = 700
        x = (WIDTH - window_width) // 2
        y = (HEIGHT - window_height) // 2

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
        """Dodaje gracza do bazy danych.

        Args:
            nickname: Pseudonim gracza.
            password: Hasło gracza.
        """
        session = Session()
        max_id = session.query(func.max(Player.id_player)).scalar()
        max_id = max_id or 0
        max_id = int(max_id)
        session.add(Player(max_id + 1, nickname, hash_password(password)))
        session.commit()
        self.destroy()
        messagebox.showinfo("Rejestracja", "Zarejestrowano pomyślnie!")


class LoginWindow(tk.Tk):
    """Klasa reprezentuje ekran logowania graczy.

    Args:
        master: Nadrzędne okno główne.
    """

    def __init__(self, master: StartWindow) -> None:
        super().__init__()
        self.title("Rejestracja")

        window_width = 600
        window_height = 700
        x = (WIDTH - window_width) // 2
        y = (HEIGHT - window_height) // 2

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

    def check_in_db(self, nickname: str, password: str, master: StartWindow) -> None:
        """Sprawdza czy gracz o podanych danych znajduje się w bazie.

        Args:
            nickname: Pseudonim gracza.
            password: Hasło gracza.
            master: Nadrzędne okno główne.
        """
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
    """Klasa reprezentuje ekran statystyk graczy."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Rejestracja")

        window_width = 600
        window_height = 700
        x = (WIDTH - window_width) // 2
        y = (HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        session = Session()
        self.players = session.query(Player).all()
        self.players = sorted(self.players, key=lambda player: player.id_player)
        session.close()

        title_label = tk.Label(self, text="Statystyki graczy", font=("Comic sans MS", 20), pady=30, bg=BG_COLOR)
        title_label.pack()

        tree = ttk.Treeview(self, height=20)
        tree["columns"] = ("Nickname", "BestScore")
        tree.heading("#0", text="ID")
        tree.heading("Nickname", text="Nazwa użytkownika")
        tree.heading("BestScore", text="Wynik")

        tree.column("#0", width=50, minwidth=50, anchor=tk.CENTER)
        tree.column("Nickname", width=300, minwidth=300, anchor=tk.CENTER)
        tree.column("BestScore", width=50, minwidth=50, anchor=tk.CENTER)

        i = 1
        for player in self.players:
            tree.insert("", "end", text=f"{i}", values=(player.nickname, player.best_score))
            i += 1

        tree.pack(padx=50)

        export_button = tk.Button(self, text="EKSPORTUJ", font=BUTTON_FONT, command=self.export, width=12, height=1,
                                  bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        export_button.place(x=140, y=600)

        go_back_button = tk.Button(self, text="POWRÓT", font=BUTTON_FONT, command=self.destroy, width=12, height=1,
                                   bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        go_back_button.place(x=350, y=600)

    def export(self) -> None:
        """Eksportuje dane graczy do pliku .csv."""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["IdPlayer", "Nickname", "BestScore"])
            for player in self.players:
                writer.writerow([player.id_player, player.nickname, player.best_score])
        messagebox.showinfo("Sukces", "Importowanie zakończone sukcesem!")


class OptionsWindow(tk.Tk):
    """Klasa reprezentuje ekran opcji.

    Args:
        master: Nadrzędne okno główne.

    Attributes:
        master (StartWindow): Nadrzędne okno główne.
        elements (list[str]): Lista mozliwych wyborów gracza.
        difficulty (int): Poziom trudności: 0 - klasyczny, 1 - hradcore.

    """

    def __init__(self, master: StartWindow) -> None:
        super().__init__()
        self.title("Opcje")

        self.master = master

        window_width = 600
        window_height = 500
        x = (WIDTH - window_width) // 2
        y = (HEIGHT - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.config(bg=BG_COLOR)

        title_label = tk.Label(self, text="OPCJE", font=("Comic sans MS", 50), pady=30, bg=BG_COLOR)
        title_label.pack()

        self.elements = ["Tryb klasyczny", "Tryp hardcore"]
        selected = tk.IntVar()

        self.difficulty = 0

        for i, element in enumerate(self.elements):
            radiobutton = tk.Radiobutton(self, text=element, variable=selected, value=i,
                                         command=lambda i=i: self.select_option(i), bg=BG_COLOR,
                                         activebackground=BG_COLOR,
                                         font=FORM_BUTTON_FONT)
            radiobutton.pack()

        confirm_button = tk.Button(self, text="POTWIERDŹ", font=BUTTON_FONT, command=self.destroy, width=12, height=1,
                                   bg=BUTTON_COLOR, activebackground=BUTTON_COLOR)
        confirm_button.pack(pady=50)

    def select_option(self, index: int) -> None:
        """Przekazuje nadrzędnemu oknu poziom trudności wybrany przez gracza.

        Args:
            index: Indeks opcji.

        """
        self.master.difficulty = index
