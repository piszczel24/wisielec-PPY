from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("postgresql://pycharm:pycharm@localhost:5432/postgres", echo=True)


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


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    word = Column(String(50), nullable=False)
    category_id = Column(Integer, nullable=False)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


def db_initialize():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Category).count() == 0 and session.query(Word).count() == 0:
        categories = [
            Category(name='Sport'),
            Category(name='Muzyka'),
            Category(name='Film'),
            Category(name='Historia'),
            Category(name='Nauka'),
            Category(name='Sztuka'),
            Category(name='Gastronomia'),
            Category(name='Literatura'),
            Category(name='Podróże'),
            Category(name='Technologia')
        ]

        session.add_all(categories)
        session.commit()

        words = [
            Word(word='Piłka', category_id=1),
            Word(word='Koszykówka', category_id=1),
            Word(word='Tenis', category_id=1),
            Word(word='Boks', category_id=1),
            Word(word='Pływanie', category_id=1),
            Word(word='Siatkówka', category_id=1),
            Word(word='Hokej', category_id=1),
            Word(word='Golf', category_id=1),
            Word(word='Bieganie', category_id=1),
            Word(word='Judo', category_id=1),
            Word(word='Rock', category_id=2),
            Word(word='Pop', category_id=2),
            Word(word='Hip-hop', category_id=2),
            Word(word='Jazz', category_id=2),
            Word(word='Metal', category_id=2),
            Word(word='Klasyczna', category_id=2),
            Word(word='Reggae', category_id=2),
            Word(word='Elektroniczna', category_id=2),
            Word(word='Country', category_id=2),
            Word(word='Dramat', category_id=3),
            Word(word='Komedia', category_id=3),
            Word(word='Akcji', category_id=3),
            Word(word='Thriller', category_id=3),
            Word(word='Horror', category_id=3),
            Word(word='Animowany', category_id=3),
            Word(word='Romans', category_id=3),
            Word(word='Western', category_id=3),
            Word(word='Dokumentalny', category_id=3),
            Word(word='Starożytność', category_id=4),
            Word(word='Średniowiecze', category_id=4),
            Word(word='Renasans', category_id=4),
            Word(word='Nowożytność', category_id=4),
            Word(word='Rewolucje', category_id=4),
            Word(word='Fizyka', category_id=5),
            Word(word='Biologia', category_id=5),
            Word(word='Chemia', category_id=5),
            Word(word='Matematyka', category_id=5),
            Word(word='Astronomia', category_id=5),
            Word(word='Psychologia', category_id=5),
            Word(word='Geologia', category_id=5),
            Word(word='Informatyka', category_id=5),
            Word(word='Ekologia', category_id=5),
            Word(word='Genetyka', category_id=5),
            Word(word='Malarstwo', category_id=6),
            Word(word='Rzeźba', category_id=6),
            Word(word='Fotografia', category_id=6),
            Word(word='Teatr', category_id=6),
            Word(word='Taniec', category_id=6),
            Word(word='Architektura', category_id=6),
            Word(word='Literatura', category_id=6),
            Word(word='Film', category_id=6),
            Word(word='Grafika', category_id=6),
            Word(word='Design', category_id=6),
            Word(word='Pizza', category_id=7),
            Word(word='Sushi', category_id=7),
            Word(word='Kebab', category_id=7),
            Word(word='Pierogi', category_id=7),
            Word(word='Spaghetti', category_id=7),
            Word(word='Burgery', category_id=7),
            Word(word='Lody', category_id=7),
            Word(word='Ramen', category_id=7),
            Word(word='Curry', category_id=7),
            Word(word='Zapiekanka', category_id=7),
            Word(word='Powieść', category_id=8),
            Word(word='Poezja', category_id=8),
            Word(word='Dramat', category_id=8),
            Word(word='Biografia', category_id=8),
            Word(word='Fantastyka', category_id=8),
            Word(word='Kryminał', category_id=8),
            Word(word='Romans', category_id=8),
            Word(word='Nowela', category_id=8),
            Word(word='Esej', category_id=8),
            Word(word='Plaża', category_id=9),
            Word(word='Góry', category_id=9),
            Word(word='Miasto', category_id=9),
            Word(word='Wyspa', category_id=9),
            Word(word='Pustynia', category_id=9),
            Word(word='Jezioro', category_id=9),
            Word(word='Zabytki', category_id=9),
            Word(word='Wodospad', category_id=9),
            Word(word='Krajobraz', category_id=9),
            Word(word='Komputer', category_id=10),
            Word(word='Smartfon', category_id=10),
            Word(word='Internet', category_id=10),
            Word(word='Programowanie', category_id=10),
            Word(word='Cyberbezpieczeństwo', category_id=10),
            Word(word='Gaming', category_id=10)
        ]

        session.add_all(words)
        session.commit()
