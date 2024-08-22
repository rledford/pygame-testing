from core.game import Game
from objects.player import Player

game = Game()
player = Player(
    game,
    {
        "position": [400, 300],
        "speed": 400,
        "accel": 2700,
        "gravity": 1800,
        "hitbox": [0, 0, 32, 32],
    },
)
game.run()
