import pygame
import sys

from core.bus import EventBus
from core.entity import Entity
from core.event import GameActionEvent

class Game():
    __FPS = 60
    __REFRESH = pygame.USEREVENT

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("test")
        pygame.time.set_timer(Game.__REFRESH, int(1000.0/Game.__FPS))

        self.screen = pygame.display.set_mode((800,600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.entities: dict[int, Entity] = {}
        self.tilemap: dict[str, dict] = {}

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity

    def update(self):
        for e in self.entities.values():
            e.update(self.dt)
        self.dt = self.clock.tick(Game.__FPS) / 1000.0

    def draw(self):
        self.screen.fill((0,0,0))
        for e in self.entities.values():
            e.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        EventBus.broadcast(
                            GameActionEvent.from_pygame_key_event(key=event.key, pressed=True)
                        )
                if event.type == pygame.KEYUP:
                    EventBus.broadcast(
                        GameActionEvent.from_pygame_key_event(key=event.key, pressed=False)
                    )
                if event.type == Game.__REFRESH:
                    self.draw()
            self.update()


        pygame.quit()
        sys.exit()

