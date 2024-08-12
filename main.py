from core.game import Game
from objects.player import Player

game = Game()
player = Player()
game.add_entity(player)
game.run()
