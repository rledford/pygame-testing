from typing_extensions import Optional, NotRequired
import pygame
from core.entity import PhysicsEntity, PhysicsEntityProps
from core.events import (
    A_DOWN,
    A_LEFT,
    A_RIGHT,
    A_UP,
    E_INPUT,
    GameActionEvent,
    GameEvent,
)
from core.game import Game


class PlayerProps(PhysicsEntityProps):
    speed: NotRequired[float]
    accel: NotRequired[float]
    decel: NotRequired[float]
    max_fall_speed: NotRequired[float]


class Player(PhysicsEntity):
    def __init__(self, game: Game, props: Optional[PlayerProps] = None):
        super().__init__()
        self.game = game
        self.move_x: list[float] = [0, 0]
        self.move_y: list[float] = [0, 0]
        self.speed = 30
        self.accel = 900
        self.decel = 900
        self.gravity = 10
        self.max_fall_speed = 50
        self.grounded = False

        self.game.router.on(E_INPUT, self.id, self.handle_event)
        self.game.add_entity(self)

        self.set_props(props)

    @property
    def dx(self):
        return self.move_x[0] + self.move_x[1]

    @property
    def dy(self):
        return self.move_y[0] + self.move_y[1]

    def update(self, dt: float):
        self.x += self.dx * self.speed * dt

    def apply_gravity(self, dt: float):
        if self.grounded:
            return

        self.move_y[1] = min(self.move_y[1] + self.gravity * dt, self.max_fall_speed)

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
        pygame.draw.circle(surface, (255, 0, 0), self.position, 25)

    def handle_event(self, event: GameEvent):
        if isinstance(event, GameActionEvent):
            self.handle_action(event)
