class PlayerDto:
    def __init__(self, id_player: int, nickname: str) -> None:
        self.id_player = id_player
        self.nickname = nickname
        self.max_score = 0
