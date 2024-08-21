from core.game import Game
from objects.player import Player

game = Game()
player = Player(game, {"position": [400, 300], "speed": 100})
game.run()
