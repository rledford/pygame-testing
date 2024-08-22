import pygame
import sys

from core.entity import Entity, PhysicsEntity
from core.event_router import GameEventRouter
from core.events import (
    A_ACTIVATE,
    A_DOWN,
    A_JUMP,
    A_LEFT,
    A_NONE,
    A_RIGHT,
    A_UP,
    E_RENDER,
    GameActionEvent,
)

FPS = 120
V_WIDTH = 800
V_HEIGHT = 600
PYGAME_KEY_ACTION_MAP = {
    # left
    pygame.K_a: A_LEFT,
    pygame.K_LEFT: A_LEFT,
    # right
    pygame.K_d: A_RIGHT,
    pygame.K_RIGHT: A_RIGHT,
    # up
    pygame.K_w: A_UP,
    pygame.K_UP: A_UP,
    # down
    pygame.K_s: A_DOWN,
    pygame.K_DOWN: A_DOWN,
    # jump
    pygame.K_SPACE: A_JUMP,
    # activate
    pygame.K_e: A_ACTIVATE,
}


def pygame_key_to_game_action(key: int) -> int:
    return PYGAME_KEY_ACTION_MAP.get(key, A_NONE)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("test")
        pygame.time.set_timer(E_RENDER, int(1000.0 / FPS))

        self.screen = pygame.display.set_mode((V_WIDTH, V_HEIGHT))
        self.router = GameEventRouter()
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.entities: dict[int, Entity] = {}
        self.map: dict[str, dict] = {}
        self.platforms: list[PhysicsEntity] = [
            PhysicsEntity({"position": [100, 500], "static": True}),
            PhysicsEntity({"position": [0, 400], "static": True}),
            PhysicsEntity({"position": [-100, 300], "static": True}),
        ]

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity

    def update(self):
        for e in self.entities.values():
            e.update(self.dt)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for e in self.entities.values():
            e.draw(self.screen)
        for p in self.platforms:
            p.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.router.broadcast(
                            GameActionEvent(
                                action=pygame_key_to_game_action(event.key),
                                pressed=True,
                            )
                        )
                if event.type == pygame.KEYUP:
                    self.router.broadcast(
                        GameActionEvent(
                            action=pygame_key_to_game_action(event.key), pressed=False
                        )
                    )
                if event.type == E_RENDER:
                    self.draw()
            self.update()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
