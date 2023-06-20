from game import Game
from player import Player

if __name__ == "__main__":
    player1 = Player(1, "A")
    player2 = Player(2, "B")

    game = Game(player1, player2)
    game.run()
