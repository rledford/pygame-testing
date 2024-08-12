import pygame
from core.bus import EventBus
from core.entity import Entity
from core.event import A_DOWN, A_LEFT, A_RIGHT, A_UP, E_ACTION, GameActionEvent, GameEvent

class Player(Entity):
    def __init__(self):
        Entity.__init__(self, [100,200])
        self.move_x = [0, 0]
        self.move_y = [0, 0]
        self.speed = 30
        self.gravity = 50
        EventBus.on(E_ACTION, self.id, self.on_message)

    @property
    def dx(self):
        return self.move_x[0] + self.move_x[1]

    @property
    def dy(self):
       return self.move_y[0] + self.move_y[1]

    def update(self, dt: float):
        self.position[0] += self.dx * self.speed * dt
        self.position[1] += self.dy * self.speed * dt

    def handle_action(self, event: GameActionEvent):
        if event.action == A_LEFT:
            self.move_x[0] = -1 if event.pressed else 0
        elif event.action == A_RIGHT:
            self.move_x[1] = 1 if event.pressed else 0
        elif event.action == A_UP:
            self.move_y[0] = -1 if event.pressed else 0
        elif event.action == A_DOWN:
            self.move_y[1] = 1 if event.pressed else 0

    def draw(self, surface):
        pygame.draw.circle(surface, (255,0,0), self.position, 25)

    def on_message(self, event: GameEvent):
        if isinstance(event, GameActionEvent):
            self.handle_action(event)

