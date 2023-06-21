DROP TABLE IF EXISTS Word;
DROP TABLE IF EXISTS Category;

CREATE TABLE Category (
  IdCategory SERIAL PRIMARY KEY,
  Name VARCHAR(50) NOT NULL
);

INSERT INTO Category (Name)
VALUES
  ('Sport'),
  ('Muzyka'),
  ('Film'),
  ('Historia'),
  ('Nauka'),
  ('Sztuka'),
  ('Gastronomia'),
  ('Literatura'),
  ('Podróże'),
  ('Technologia');

CREATE TABLE Word (
  IdWord SERIAL PRIMARY KEY,
  Word VARCHAR(50) NOT NULL,
  IdCategory INTEGER REFERENCES Category(IdCategory)
);

INSERT INTO Word (Word, IdCategory)
VALUES
  -- Sport
  ('Piłka', 1),
  ('Koszykówka', 1),
  ('Tenis', 1),
  ('Boks', 1),
  ('Pływanie', 1),
  ('Siatkówka', 1),
  ('Hokej', 1),
  ('Golf', 1),
  ('Bieganie', 1),
  ('Judo', 1),

  -- Muzyka
  ('Rock', 2),
  ('Pop', 2),
  ('Hip-hop', 2),
  ('Jazz', 2),
  ('Metal', 2),
  ('Klasyczna', 2),
  ('Reggae', 2),
  ('R&B', 2),
  ('Elektroniczna', 2),
  ('Country', 2),

  -- Film
  ('Dramat', 3),
  ('Komedia', 3),
  ('Akcji', 3),
  ('Thriller', 3),
  ('Horror', 3),
  ('Sci-fi', 3),
  ('Animowany', 3),
  ('Romans', 3),
  ('Western', 3),
  ('Dokumentalny', 3),

  -- Historia
  ('Starożytność', 4),
  ('Średniowiecze', 4),
  ('Renasans', 4),
  ('Nowożytność', 4),
  ('Wojny światowe', 4),
  ('Zimna wojna', 4),
  ('Epoka Oświecenia', 4),
  ('Era kolonialna', 4),
  ('Imperium Rzymskie', 4),
  ('Rewolucje', 4),

  -- Nauka
  ('Fizyka', 5),
  ('Biologia', 5),
  ('Chemia', 5),
  ('Matematyka', 5),
  ('Astronomia', 5),
  ('Psychologia', 5),
  ('Geologia', 5),
  ('Informatyka', 5),
  ('Ekologia', 5),
  ('Genetyka', 5),

  -- Sztuka
  ('Malarstwo', 6),
  ('Rzeźba', 6),
  ('Fotografia', 6),
  ('Teatr', 6),
  ('Taniec', 6),
  ('Architektura', 6),
  ('Literatura', 6),
  ('Film', 6),
  ('Grafika', 6),
  ('Design', 6),

-- Gastronomia
  ('Pizza', 7),
  ('Sushi', 7),
  ('Kebab', 7),
  ('Pierogi', 7),
  ('Spaghetti', 7),
  ('Burgery', 7),
  ('Lody', 7),
  ('Ramen', 7),
  ('Curry', 7),
  ('Zapiekanka', 7),

  -- Literatura
  ('Powieść', 8),
  ('Poezja', 8),
  ('Dramat', 8),
  ('Biografia', 8),
  ('Fantastyka', 8),
  ('Kryminał', 8),
  ('Literatura dziecięca', 8),
  ('Romans', 8),
  ('Nowela', 8),
  ('Esej', 8),

  -- Podróże
  ('Plaża', 9),
  ('Góry', 9),
  ('Miasto', 9),
  ('Wyspa', 9),
  ('Pustynia', 9),
  ('Jezioro', 9),
  ('Park narodowy', 9),
  ('Zabytki', 9),
  ('Wodospad', 9),
  ('Krajobraz', 9),

  -- Technologia
  ('Komputer', 10),
  ('Smartfon', 10),
  ('Internet', 10),
  ('Sztuczna inteligencja', 10),
  ('Sieci społecznościowe', 10),
  ('Programowanie', 10),
  ('E-commerce', 10),
  ('Big Data', 10),
  ('Cyberbezpieczeństwo', 10),
  ('Gaming', 10);

COMMIT;
